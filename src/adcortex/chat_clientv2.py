"""Chat Client V2 for ADCortex API with sequential message processing"""

import asyncio
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
from uuid import uuid4

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError

from .types import Ad, AdResponse, Message, Role, SessionInfo

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONTEXT_TEMPLATE = "Here is a product the user might like: {ad_title} - {ad_description}: here is a sample way to present it: {placement_template}"
AD_FETCH_URL = "https://adcortex.3102labs.com/ads/matchv2"

# Configure logging
logger = logging.getLogger(__name__)

class AdcortexChatClientV2:
    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        timeout: Optional[int] = 3,
        log_level: Optional[int] = logging.ERROR,
        disable_logging: bool = False,
    ):
        self._session_info = session_info
        self._context_template = context_template
        self._api_key = api_key or os.getenv("ADCORTEX_API_KEY")
        self._headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self._api_key,
        }
        self._timeout = timeout
        self.latest_ad = None
        self._disable_logging = disable_logging
        
        # Message processing queue
        self._message_queue: List[Message] = []
        self._is_processing = False
        self._processing_task = None

        # Configure logging
        if not disable_logging:
            logger.setLevel(log_level)
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        if not self._api_key:
            raise ValueError("ADCORTEX_API_KEY is not set and not provided")

    def _log_info(self, message: str) -> None:
        """Log info message if logging is enabled."""
        if not self._disable_logging:
            logger.info(message)

    def _log_error(self, message: str) -> None:
        """Log error message if logging is enabled."""
        if not self._disable_logging:
            logger.error(message)

    async def __call__(self, role: Role, content: str) -> None:
        """Add a message to the queue and process it."""
        current_message = Message(
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc).timestamp()
        )
        self._message_queue.append(current_message)
        self._log_info(f"Message queued: {role} - {content}")

        if not self._is_processing:
            self._is_processing = True
            self._processing_task = asyncio.create_task(self._process_queue())
            await self._processing_task
            return
        
        # If already processing, wait for the current task to complete
        if self._processing_task and not self._processing_task.done():
            await self._processing_task
        
        # Create a new task for the remaining messages
        self._processing_task = asyncio.create_task(self._process_queue())
        await self._processing_task

    async def _process_queue(self) -> None:
        """Process messages in the queue one at a time."""
        try:
            while self._message_queue:
                message = self._message_queue[0]
                self._log_info(f"Processing message: {message.content}")
                
                try:
                    await self._fetch_ad(message)
                    self._message_queue.pop(0)
                except Exception as e:
                    self._log_error(f"Error processing message: {e}")
                    self._message_queue.pop(0)
        finally:
            self._is_processing = False

    async def _fetch_ad(self, current_message: Message) -> None:
        """Fetch an ad based on the current message asynchronously."""
        payload = self._prepare_payload(current_message)
        await self._send_request(payload)

    def _prepare_payload(self, current_message: Message) -> Dict[str, Any]:
        """Prepare the payload for the ad request."""
        return {
            "RGUID": str(uuid4()),
            "session_info": self._session_info.model_dump(),
            "user_data": self._session_info.user_info.model_dump(),
            "messages": [current_message.model_dump()],
        }

    async def _send_request(self, payload: Dict[str, Any]) -> None:
        """Send the request to the ADCortex API asynchronously."""
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(
                    AD_FETCH_URL,
                    headers=self._headers,
                    json=payload
                )
                response.raise_for_status()
                await self._handle_response(response.json())
        except httpx.TimeoutException:
            self._log_error("Request timed out")
        except httpx.RequestError as e:
            self._log_error(f"Error fetching ad: {e}")

    async def _handle_response(self, response_data: Dict[str, Any]) -> None:
        """Handle the response from the ad request."""
        try:
            parsed_response = AdResponse(**response_data)
            if parsed_response.ads:
                self.latest_ad = parsed_response.ads[0]
                self._log_info(f"Ad fetched: {self.latest_ad.ad_title}")
            else:
                self._log_info("No ads returned")
        except ValidationError as e:
            self._log_error(f"Invalid ad response format: {e}")

    def create_context(self) -> str:
        """Create a context string for the last seen ad."""
        if self.latest_ad:
            return self._context_template.format(**self.latest_ad.model_dump())
        return ""

    def get_latest_ad(self) -> Optional[Ad]:
        """Get the latest ad."""
        return self.latest_ad 
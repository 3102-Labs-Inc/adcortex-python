"""Chat Client for ADCortex API"""

import os
import uuid  # Import the uuid module
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional

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


class AdcortexChatClient:
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

    def __call__(self, role: Role, content: str) -> Optional[Dict[str, Any]]:
        """Add a message and fetch an ad if applicable."""
        current_message = Message(
            role=role, content=content, timestamp=datetime.now(timezone.utc).timestamp()
        )
        self._log_info(f"Message added: {role} - {content}")

        return self._fetch_ad(current_message)

    def _fetch_ad(self, current_message: Message) -> Optional[Dict[str, Any]]:
        """Fetch an ad based on the current messages."""

        payload = self._prepare_payload(current_message)
        response_data = self._send_request(payload)

        if response_data:
            return self._handle_response(response_data)
        return None

    def _prepare_payload(self, current_message: Message) -> Dict[str, Any]:
        """Prepare the payload for the ad request."""

        payload = {
            "RGUID": str(uuid.uuid4()),
            "session_info": self._session_info.model_dump(),
            "user_data": self._session_info.user_info.model_dump(),
            "messages": [current_message.model_dump()],
        }
        return payload

    def _send_request(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send the request to the ADCortex API and return the response."""
        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    AD_FETCH_URL,
                    headers=self._headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            self._log_error("Request timed out")
            return None
        except httpx.RequestError as e:
            self._log_error(f"Error fetching ad: {e}")
            return None

    def _handle_response(
        self, response_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Handle the response from the ad request."""
        try:
            parsed_response = AdResponse(**response_data)
            if parsed_response.ads:
                self.latest_ad = parsed_response.ads[0]
                self._log_info(f"Ad fetched: {self.latest_ad.ad_title}")
                return self.latest_ad
            self._log_info("No ads returned")
            return {}
        except ValidationError as e:
            self._log_error(f"Invalid ad response format: {e}")
            return {}

    def create_context(self) -> str:
        """Create a context string for the last seen ad."""
        if self.latest_ad:
            return self._context_template.format(**self.latest_ad.model_dump())
        return ""

    def get_latest_ad(self) -> Optional[Ad]:
        """Get the latest ad."""
        return self.latest_ad

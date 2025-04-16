"""Chat Client for ADCortex API"""

import asyncio
import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import aiohttp
from dotenv import load_dotenv

from .types import Ad, Message, SessionInfo

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONTEXT_TEMPLATE = "Here is a product the user might like: {ad_title} - {ad_description}: here is a sample way to present it: {placement_template}"
AD_FETCH_URL = "https://adcortex.3102labs.com/ads/matchv2"


class AdcortexChatClient:
    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        timeout: Optional[int] = 3,
    ):
        self._session_info = session_info
        self._context_template = context_template
        self._api_key = api_key or os.getenv("ADCORTEX_API_KEY")
        self._headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self._api_key,
        }
        self._timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
        self.latest_ad: Optional[Ad] = None

        if not self._api_key:
            raise ValueError("ADCORTEX_API_KEY is not set and not provided")

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    def __call__(self, role: str, content: str) -> None:
        """Add a message and asynchronously fetch an ad if applicable."""
        current_message = Message(
            role=role, content=content, timestamp=datetime.now(timezone.utc).timestamp()
        )

        asyncio.create_task(self._fetch_ad(current_message))

    async def _fetch_ad(self, current_message: Message) -> None:
        """Asynchronously fetch an ad based on the current messages."""
        if not self._session:
            self._session = aiohttp.ClientSession()

        payload = self._prepare_payload(current_message)
        try:
            async with self._session.post(
                AD_FETCH_URL, headers=self._headers, json=payload, timeout=self._timeout
            ) as response:
                response.raise_for_status()
                response_data = await response.json()
                if response_data:
                    await self._handle_response(response_data)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass  # Silently handle errors as this is a background task

    def _prepare_payload(self, current_message: Message) -> Dict[str, Any]:
        """Prepare the payload for the ad request."""
        payload = {
            "RGUID": str(uuid.uuid4()),
            "session_info": self._session_info.model_dump(),
            "user_data": self._session_info.user_info.model_dump(),
            "messages": [current_message.model_dump()],
        }
        return payload

    async def _handle_response(self, response_data: Dict[str, Any]) -> None:
        """Handle the response from the ad request."""
        ads = response_data.get("ads", [])
        if ads:
            self.latest_ad = Ad(**ads[0])

    def create_context(self) -> str:
        """Create a context string for the last seen ad."""
        if self.latest_ad:
            return self._context_template.format(**self.latest_ad.model_dump())
        return ""

    def get_latest_ad(self) -> Optional[Ad]:
        """Get the latest ad."""
        return self.latest_ad

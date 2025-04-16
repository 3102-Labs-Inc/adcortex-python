"""Asynchronous Chat Client for ADCortex API

This module provides an asynchronous implementation of the ADCortex chat client
that separates message handling from ad fetching operations.
"""

import os
import uuid
from datetime import datetime, timezone
import logging
from typing import Any, Dict, Optional, Deque
from collections import deque
import asyncio
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from pydantic import ValidationError

from .types import Ad, AdResponse, Message, Role, SessionInfo

# Load environment variables from .env file
load_dotenv()

# Constants
DEFAULT_CONTEXT_TEMPLATE = "Here is a product the user might like: {ad_title} - {ad_description}: here is a sample way to present it: {placement_template}"
AD_FETCH_URL = "https://adcortex.3102labs.com/ads/matchv2"
MAX_QUEUE_SIZE = 100  # Maximum number of queued requests
MAX_CONCURRENT_REQUESTS = 1  # Limit to one request at a time

# Configure logging
logger = logging.getLogger(__name__)


class AsyncAdcortexChatClient:
    """
    Asynchronous implementation of the ADCortex chat client.
    
    This client processes messages sequentially while maintaining efficient resource usage.
    """

    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        timeout: Optional[int] = 3,
        log_level: Optional[int] = logging.ERROR,
        disable_logging: bool = False,
    ):
        """
        Initialize the async chat client.
        """
        self._session_info = session_info
        self._context_template = context_template
        self._api_key = api_key or os.getenv("ADCORTEX_API_KEY")
        self._headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self._api_key,
        }
        self._timeout = timeout
        self._disable_logging = disable_logging
        
        # State management
        self._latest_ad: Optional[Ad] = None
        self._last_fetch_time = 0
        self._first_get = True
        
        # Request queue and processing
        self._request_queue: Deque[Message] = deque(maxlen=MAX_QUEUE_SIZE)
        self._shutdown_event = asyncio.Event()
        self._processing_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self._processing_task: Optional[asyncio.Task] = None

        # Configure logging
        if not disable_logging:
            logger.setLevel(log_level)
            if not logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
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

    def __call__(self, role: Role, content: str) -> None:
        """
        Process a new message and trigger async ad fetch.
        Messages are queued and processed sequentially.
        """
        current_message = Message(
            role=role, 
            content=content, 
            timestamp=datetime.now(timezone.utc).timestamp()
        )
        self._log_info(f"Message added: {role} - {content}")
        
        # Add to queue if there's space
        if len(self._request_queue) >= MAX_QUEUE_SIZE:
            self._log_error("Request queue full, dropping message")
            return
            
        self._request_queue.append(current_message)
        self._log_info(f"Queue size: {len(self._request_queue)}")
        
        # Start processing if not already running
        if not self._processing_task or self._processing_task.done():
            self._processing_task = asyncio.create_task(self._process_queue())

    async def _process_queue(self) -> None:
        """Process messages from the queue sequentially."""
        while self._request_queue and not self._shutdown_event.is_set():
            async with self._processing_semaphore:
                message = self._request_queue.popleft()
                await self._fetch_ad(message)
                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.1)

    async def _fetch_ad(self, message: Message) -> None:
        """Fetch an ad for a single message."""
        try:
            payload = {
                "RGUID": str(uuid.uuid4()),
                "session_info": self._session_info.model_dump(),
                "user_data": self._session_info.user_info.model_dump(),
                "messages": [message.model_dump()],
            }

            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(
                    AD_FETCH_URL,
                    headers=self._headers,
                    json=payload
                )
                response.raise_for_status()
                response_data = response.json()

                try:
                    parsed_response = AdResponse(**response_data)
                    if parsed_response.ads:
                        self._latest_ad = parsed_response.ads[0]
                        self._log_info(f"Ad fetched: {self._latest_ad.ad_title}")
                    else:
                        self._log_info("No ads returned")
                except ValidationError as e:
                    self._log_error(f"Invalid ad response format: {e}")
        except Exception as e:
            self._log_error(f"Error fetching ad: {e}")
        finally:
            self._last_fetch_time = datetime.now(timezone.utc).timestamp()

    def get_latest_ad(self) -> Optional[Dict[str, Any]]:
        """
        Get the latest ad if available and updated.
        """
        if self._latest_ad:
            if self._first_get:
                self._first_get = False
                return self._latest_ad.model_dump()
            if self._last_fetch_time > 0:
                ad_data = self._latest_ad.model_dump()
                self._last_fetch_time = 0  # Reset to prevent returning the same ad
                return ad_data
        return None

    def create_context(self) -> str:
        """
        Create a context string for the last seen ad.
        """
        if self._latest_ad:
            return self._context_template.format(**self._latest_ad.model_dump())
        return ""

    async def wait_for_queue(self) -> None:
        """Wait for all queued messages to be processed."""
        while self._request_queue and not self._shutdown_event.is_set():
            await asyncio.sleep(0.1)

    async def cleanup(self) -> None:
        """
        Cleanup resources used by the client.
        """
        self._shutdown_event.set()
        if self._processing_task and not self._processing_task.done():
            await self._processing_task

    @asynccontextmanager
    async def context(self):
        """
        Async context manager for the client.
        """
        try:
            yield self
        finally:
            await self.cleanup()
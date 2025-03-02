"""Chat Client for ADCortex API"""
import os
from typing import Optional, List
import requests
from dataclasses import asdict
from dotenv import load_dotenv
from src.adcortex.types import SessionInfo, Message, Ad

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONTEXT_TEMPLATE = ""

class AdcortexChatClient:
    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        num_messages_before_ad: int = 3,
        num_messages_between_ads: int = 2,
    ):
        self.session_info = session_info
        self.context_template = context_template
        self.api_key = api_key or os.getenv("ADCORTEX_API_KEY")
        self.base_url = "https://adcortex.3102labs.com/ads/match"

        if not self.api_key:
            raise ValueError("ADCORTEX_API_KEY is not set and not provided")

        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

        self.messages: List[Message] = []
        self.num_messages_before_ad = num_messages_before_ad
        self.num_messages_between_ads = num_messages_between_ads
        self.last_ad_seen: Optional[Ad] = None

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation."""
        self.messages.append(Message(role=role, content=content))

    def fetch_ad(self) -> dict:
        """Fetch an ad based on the current messages."""
        if len(self.messages) < self.num_messages_before_ad:
            return {"ads": []}  # Not enough messages to fetch an ad

        payload = {
            "RGUID": self.session_info.session_id,  # Assuming session_id is used as RGUID
            "session_info": asdict(self.session_info),
            "user_data": asdict(self.session_info.user_info),  # Include user data
            "messages": [asdict(message) for message in self.messages[-self.num_messages_before_ad:]],
            "platform": asdict(self.session_info.platform),  # Include platform information
        }

        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        # Check if ads are returned
        ads = response_data.get("ads", [])
        if ads:
            self.last_ad_seen = Ad(**ads[0])  # Store the last ad seen
        return response_data

    def should_show_ad(self) -> bool:
        """Determine if an ad should be shown based on message count."""
        return len(self.messages) % (self.num_messages_before_ad + self.num_messages_between_ads) == 0 
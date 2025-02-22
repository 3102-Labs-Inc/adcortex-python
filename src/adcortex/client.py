"""Client for ADCortex API"""
import os
from typing import Optional, List
import requests
from dataclasses import asdict

from adcortex.types import SessionInfo, Message, Ad


# TODO: Fill up the Default Context Template
DEFAULT_CONTEXT_TEMPLATE = """

"""

class AdcortexClient:
    def __init__(
        self,
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
    ):
        self.session_info = session_info
        self.context_template = context_template
        self.api_key = api_key or os.getenv("ADCORTES_API_KEY")
        self.base_url = "https://adcortex.3102labs.com/ads/match"

        if not self.api_key:
            raise ValueError("ADCORTES_API_KEY is not set and not provided")
        
        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

    def _generate_payload(self, messages: List[Message]) -> dict:
        payload = {
            "session_info": asdict(self.session_info),
            "messages": [asdict(message) for message in messages]
        }
        return payload
    
    # NOTE: @Rahul review this for functionality
    def fetch_ad(self, messages: List[Message]) -> Ad:
        payload = self._generate_payload(messages)
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return Ad(**response.json())

    # NOTE: @Rahul review this for functionality
    def generate_context(self, ad: Ad) -> str:
        return self.context_template.format(
            ad_title=ad.ad_title,
            ad_description=ad.ad_description,
            placement_template=ad.placement_template,
            link=ad.link,
        )

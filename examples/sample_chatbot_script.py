# import sys
# import os

# sys.path.append("../src")

from adcortex.chat_client import AdcortexChatClient
from adcortex.types import Message, Platform, SessionInfo, UserInfo

# Initialize the chat client
session_info = SessionInfo(
    session_id="fads-fda",
    character_name="Alex",
    character_metadata={"description": "Friendly and humorous assistant"},
    user_info=UserInfo(
        user_id="12345", age=20, gender="male", location="US", interests=["all"]
    ),
    platform=Platform(name="ChatBotX", version="1.0.2"),
)

# Initialize the chat client
chat_client = AdcortexChatClient(
    session_info=session_info, num_messages_before_ad=3, num_messages_between_ads=10
)

# Simulate adding messages and automatically check for ads
ad_response = chat_client(role="user", content="I'm looking for a new gaming setup.")
if ad_response:
    print(ad_response)

ad_response = chat_client(role="ai", content="What features are you looking for?")
if ad_response:
    print(ad_response)

ad_response = chat_client(role="user", content="I need something ergonomic.")
if ad_response:
    print(ad_response)

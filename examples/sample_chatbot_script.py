# import sys
# import os

# sys.path.append("../src")

from adcortex.chat_client import AdcortexChatClient
from adcortex.types import Interest, Platform, Role, SessionInfo, UserInfo
import logging

# Initialize the chat client
session_info = SessionInfo(
    session_id="fads-fda",
    character_name="Alex",
    character_metadata={"description": "Friendly and humorous assistant"},
    user_info=UserInfo(
        user_id="12345", 
        age=20, 
        gender="male", 
        location="US", 
        language="en",
        interests=[Interest.gaming, Interest.technology]  # Using Interest enum values
    ),
    platform=Platform(name="ChatBotX", version="1.0.2"),
)

# Initialize the chat client with INFO level logging
chat_client = AdcortexChatClient(
    session_info=session_info,
    log_level=logging.INFO  # Enable info level logging
)

# Simulate adding messages and automatically check for ads
ad_response = chat_client(role=Role.user, content="I'm looking for a new gaming setup.")
if ad_response:
    print(f"Ad Response: {ad_response}")

ad_response = chat_client(role=Role.ai, content="What features are you looking for?")
if ad_response:
    print(f"Ad Response: {ad_response}")

ad_response = chat_client(role=Role.user, content="I need something ergonomic.")
if ad_response:
    print(f"Ad Response: {ad_response}")

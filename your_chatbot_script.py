from adcortex.chat_client import AdcortexChatClient
from adcortex.types import SessionInfo, UserInfo, Platform

# Initialize the chat client
session_info = SessionInfo(
    session_id="43253425",
    character_name="Alex",
    character_metadata={"description": "Friendly and humorous assistant"},
    user_info=UserInfo(
        user_id="12345",
        age=20,
        gender="male",
        location="US",
        language="en",
        interests=["flirting", "gaming"]
    ),
    platform=Platform(
        name="ChatBotX",
        version="1.0.2"
    )
)

chat_client = AdcortexChatClient(session_info=session_info, num_messages_before_ad=3, num_messages_between_ads=10)

# Simulate adding messages
chat_client.add_message(role="user", content="I'm looking for a new gaming setup.")
chat_client.add_message(role="ai", content="What features are you looking for?")
chat_client.add_message(role="user", content="I need something ergonomic.")

# Check if an ad should be shown and fetch it
if chat_client.should_show_ad():
    ad_response = chat_client.fetch_ad()
    print(ad_response) 
Usage
=====

Below is a sample script that demonstrates how to initialize the chat client, add messages, and automatically check for ads:

.. code-block:: python

    from adcortex.chat_client import AdcortexChatClient
    from adcortex.types import SessionInfo, UserInfo, Platform, Message

    # Initialize the session and user info
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

    # Create the chat client instance.
    chat_client = AdcortexChatClient(
        session_info=session_info,
        num_messages_before_ad=3,
        num_messages_between_ads=10
    )

    # Simulate conversation and check for ad responses
    ad_response = chat_client(role="user", content="I'm looking for a new gaming setup.")
    if ad_response:
        print(ad_response)

    ad_response = chat_client(role="ai", content="What features are you looking for?")
    if ad_response:
        print(ad_response)

    ad_response = chat_client(role="user", content="I need something ergonomic.")
    if ad_response:
        print(ad_response)

This script shows how the client accumulates messages and fetches an ad when the specified message thresholds are met.

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

Additionally, here is an example of using the AdcortexClient to fetch ads based on a list of messages:

.. code-block:: python

    import time
    import json
    from adcortex.client import AdcortexClient
    from adcortex.types import SessionInfo, UserInfo, Platform, Message

    # Initialize the client
    session_info = SessionInfo(
        session_id="43253425",
        character_name="Alex",
        character_metadata={"description": "Friendly and humorous assistant"},
        user_info=UserInfo(
            user_id="12345",
            age=20,
            gender="male",
            location="US",
            interests=["all"]
        ),
        platform=Platform(
            name="ChatBotX",
            version="1.0.2"
        )
    )

    # Create an instance of AdcortexClient
    client = AdcortexClient(session_info=session_info)

    # Prepare messages
    messages = [
        Message(role="ai", content="I'm looking for a desk setup for my gaming. It should be more ergonomic!!"),
        Message(role="user", content="Preferably something under $500."),
        # Add more messages as needed...
    ]

    # Measure latency and fetch ad
    start_time = time.time()
    ad_response = client.fetch_ad(messages=messages)
    end_time = time.time()

    latency = end_time - start_time

    # Print the response
    print(f"Response content:")
    print(json.dumps(ad_response, default=lambda o: o.__dict__, indent=4))  # Convert Ad object to dict
    print(f"Response Time: {latency:.3f} seconds")

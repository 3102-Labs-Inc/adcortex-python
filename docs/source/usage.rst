Usage
=====

Below are examples demonstrating how to use both the synchronous and asynchronous chat clients.

Production Configuration
----------------------

For production environments, it's recommended to disable logging to improve performance:

.. code-block:: python

    # Production configuration with logging disabled
    chat_client = AdcortexChatClient(
        session_info=session_info,
        disable_logging=True,  # Disable logging in production
        timeout=5,
        max_queue_size=50
    )

Synchronous Client
-----------------

.. code-block:: python

    from adcortex.chat_client import AdcortexChatClient
    from adcortex.types import SessionInfo, UserInfo, Platform, Role, Interest, Gender

    # Initialize the session and user info
    session_info = SessionInfo(
        session_id="43253425",
        character_name="Alex",
        character_metadata="Friendly and humorous assistant",
        user_info=UserInfo(
            user_id="12345",
            age=20,
            gender=Gender.male,
            location="US",
            language="en",
            interests=[Interest.flirting, Interest.gaming]
        ),
        platform=Platform(
            name="ChatBotX",
            version="1.0.2"
        )
    )

    # Create the chat client instance
    chat_client = AdcortexChatClient(
        session_info=session_info,
        timeout=5,
        log_level=logging.INFO,
        max_queue_size=50
    )

    # Simulate conversation
    conversation = [
        (Role.ai, "I'm looking for a desk setup for my gaming. It should be more ergonomic!"),
        (Role.user, "Preferably something under $500."),
    ]

    # Process the conversation
    for role, content in conversation:
        print(f"{role.value}: {content}")
        chat_client(role=role, content=content)
        
        # Check for new ads
        latest_ad = chat_client.get_latest_ad()
        if latest_ad:
            context = chat_client.create_context()
            print("Ad context generated:")
            print(context)
        
        # Check client health
        if not chat_client.is_healthy():
            print("Client is not in a healthy state")
            break

Asynchronous Client
-----------------

.. code-block:: python

    import asyncio
    from adcortex.async_chat_client import AsyncAdcortexChatClient
    from adcortex.types import SessionInfo, UserInfo, Platform, Role, Interest, Gender

    async def main():
        # Initialize the session and user info
        session_info = SessionInfo(
            session_id="43253425",
            character_name="Alex",
            character_metadata="Friendly and humorous assistant",
            user_info=UserInfo(
                user_id="12345",
                age=20,
                gender=Gender.male,
                location="US",
                language="en",
                interests=[Interest.flirting, Interest.gaming]
            ),
            platform=Platform(
                name="ChatBotX",
                version="1.0.2"
            )
        )

        # Create the async chat client instance
        chat_client = AsyncAdcortexChatClient(
            session_info=session_info,
            timeout=10,
            log_level=logging.INFO,
            max_queue_size=50
        )

        # Simulate conversation
        conversation = [
            (Role.ai, "I'm looking for a desk setup for my gaming. It should be more ergonomic!"),
            (Role.user, "Preferably something under $500."),
        ]

        # Process the conversation
        for role, content in conversation:
            print(f"{role.value}: {content}")
            await chat_client(role=role, content=content)
            
            # Check for new ads
            latest_ad = chat_client.get_latest_ad()
            if latest_ad:
                context = chat_client.create_context()
                print("Ad context generated:")
                print(context)
            
            # Check client health
            if not chat_client.is_healthy():
                print("Client is not in a healthy state")
                break

    if __name__ == "__main__":
        asyncio.run(main())

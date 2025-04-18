"""Example script demonstrating the asynchronous AdcortexChatClient usage."""

import asyncio
import logging
from datetime import datetime
from typing import Optional

import sys
import os

sys.path.append("../src")

from adcortex.async_chat_client import AsyncAdcortexChatClient
from adcortex.types import Gender, Interest, Language, Platform, Role, SessionInfo, UserInfo

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_session_info() -> SessionInfo:
    """Create a sample session info object."""
    return SessionInfo(
        session_id=str(14149),  # Fixed session ID that works
        character_name="Alex",
        character_metadata="Friendly and humorous assistant",  # String instead of dict
        user_info=UserInfo(
            user_id="12345",
            age=20,
            gender="male",  # String value
            location="US",
            language="en",  # String value
            interests=["flirting", "gaming"]  # List of strings
        ),
        platform=Platform(name="ChatBotX", version="1.0.2")
    )

async def process_chat_interaction(
    chat_client: AsyncAdcortexChatClient,
    role: Role,
    content: str
) -> Optional[str]:
    """Process a single chat interaction and return the context if an ad was found."""
    try:
        # Send message and process queue
        await chat_client(role=role, content=content)
        
        # Check if we got a new ad
        latest_ad = chat_client.get_latest_ad()
        if latest_ad:
            return chat_client.create_context()
        return None
    except Exception as e:
        logger.error(f"Error processing chat interaction: {e}")
        return None

async def process_conversation(chat_client: AsyncAdcortexChatClient):
    """Process a simulated conversation asynchronously."""
    conversation = [
        (Role.user, "I'm looking for a new gaming laptop"),
        (Role.ai, "What's your budget and preferred screen size?"),
        (Role.user, "Around $1500 and 15-17 inches"),
        (Role.ai, "Great! Do you need it for gaming or work?"),
        (Role.user, "Mostly gaming, but some work too"),
    ]

    for role, content in conversation:
        logger.info(f"{role.value}: {content}")
        context = await process_chat_interaction(chat_client, role, content)
        
        if context:
            logger.info("Ad context generated:")
            logger.info(context)
        
        # Check client health
        if not chat_client.is_healthy():
            logger.warning("Client is not in a healthy state")
            break
        
        # Add a small delay between messages
        await asyncio.sleep(0.5)

async def main():
    """Main async function demonstrating chat client usage."""
    # Initialize the chat client
    chat_client = AsyncAdcortexChatClient(
        session_info=create_session_info(),
        log_level=logging.INFO,
        timeout=5,  # 5 second timeout for API requests
        max_queue_size=50  # Limit queue size to 50 messages
    )

    # Process the conversation
    await process_conversation(chat_client)

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 
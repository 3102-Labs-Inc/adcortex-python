"""Example script demonstrating the synchronous AdcortexChatClient usage."""

import logging
import random
from datetime import datetime
from typing import Optional

import sys
import os

sys.path.append("../src")

from adcortex.chat_client import AdcortexChatClient
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

def process_chat_interaction(chat_client: AdcortexChatClient, role: Role, content: str) -> Optional[str]:
    """Process a single chat interaction and return the context if an ad was found."""
    try:
        # Send message and process queue
        chat_client(role=role, content=content)
        
        # Check if we got a new ad
        latest_ad = chat_client.get_latest_ad()
        if latest_ad:
            return chat_client.create_context()
        return None
    except Exception as e:
        logger.error(f"Error processing chat interaction: {e}")
        return None

def main():
    """Main function demonstrating chat client usage."""
    # Initialize the chat client
    chat_client = AdcortexChatClient(
        session_info=create_session_info(),
        log_level=logging.INFO,
        timeout=5,
        max_queue_size=50
    )

    # Simulate a chat conversation
    conversation = [
        (Role.ai, "I'm looking for a desk setup for my gaming. It should be more ergonomic!"),
        (Role.user, "Preferably something under $500."),
    ]

    # Process the conversation
    for role, content in conversation:
        logger.info(f"{role.value}: {content}")
        context = process_chat_interaction(chat_client, role, content)
        
        if context:
            logger.info("Ad context generated:")
            logger.info(context)
        
        # Check client health
        if not chat_client.is_healthy():
            logger.warning("Client is not in a healthy state")
            break

if __name__ == "__main__":
    main() 
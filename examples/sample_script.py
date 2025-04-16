# import sys
# import os

# sys.path.append("../src")

import json
import time

from adcortex.direct_client import AdcortexClient
from adcortex.types import Message, Platform, SessionInfo, UserInfo

# Initialize the client
session_info = SessionInfo(
    session_id="43253425",
    character_name="Alex",
    character_metadata={"description": "Friendly and humorous assistant"},
    user_info=UserInfo(
        user_id="12345", age=20, gender="male", location="US", interests=["all"]
    ),
    platform=Platform(name="ChatBotX", version="1.0.2"),
)

# Create an instance of AdcortexClient
client = AdcortexClient(session_info=session_info)

# Prepare messages
messages = [
    Message(
        role="ai",
        content="I'm looking for a desk setup for my gaming. It should be more ergonomic!!",
    ),
    Message(role="user", content="Preferably something under $500."),
    Message(
        role="ai",
        content="I'm looking for a desk setup for my gaming. It should be more ergonomic!!",
    ),
    Message(role="user", content="Preferably something under $500."),
    Message(
        role="ai",
        content="I'm looking for a desk setup for my gaming. It should be more ergonomic!!",
    ),
    Message(role="user", content="Preferably something under $500."),
    Message(
        role="ai",
        content="I'm looking for a desk setup for my gaming. It should be more ergonomic!!",
    ),
    Message(role="user", content="Preferably something under $500."),
]

# Measure latency and fetch ad
start_time = time.time()
ad_response = client.fetch_ad(messages=messages)
end_time = time.time()

latency = end_time - start_time

# Print the response
print(f"Response content:")
print(
    json.dumps(ad_response, default=lambda o: o.__dict__, indent=4)
)  # Convert Ad object to dict
print(f"Response Time: {latency:.3f} seconds")

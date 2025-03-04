API Reference
=============

This section describes the main classes and methods of the ADCortex Chat Client library.

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   adcortex.chat_client.AdcortexChatClient

Detailed documentation for the ADCortexChatClient is provided below.

ADCortexChatClient
------------------

The :class:`adcortex.chat_client.AdcortexChatClient` is the primary interface for integrating chat-based advertising into your application.

**Constructor:**

.. code-block:: python

    AdcortexChatClient(
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        num_messages_before_ad: int = 3,
        num_messages_between_ads: int = 2,
    )

- **session_info**: Instance of :class:`adcortex.types.SessionInfo` with session, character, user, and platform details.
- **context_template**: A template string to format ad context. Default is `"Here is a product the user might like: {ad_title} - {ad_description} - {link}"`.
- **api_key**: ADCORTEX API key. If not provided, it is loaded from the environment variable.
- **num_messages_before_ad**: Number of messages before an ad is fetched.
- **num_messages_between_ads**: Number of messages to wait between ads.

**Key Methods:**

- ``__call__(role: str, content: str) -> Optional[Dict[str, Any]]``  
  Adds a message to the conversation log and checks if an ad should be fetched.

- ``_fetch_ad() -> Optional[Dict[str, Any]]``  
  Fetches an ad if the message criteria are met.

- ``_prepare_payload() -> Dict[str, Any]``  
  Prepares the JSON payload for the ad request.

- ``_send_request(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]``  
  Sends an HTTP POST request to the ADCortex API.

- ``_handle_response(response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]``  
  Processes the API response and returns ad details if available.

- ``_should_show_ad() -> bool``  
  Determines if an ad should be shown based on the message count.

- ``create_context() -> str``  
  Generates a context string using the latest fetched ad.

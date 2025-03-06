API Reference
=============

This section describes the main classes and methods of the ADCortex Chat Client library.

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   adcortex.chat_client.AdcortexChatClient
   adcortex.client.AdcortexClient

Detailed documentation for the ADCortexChatClient and AdcortexClient is provided below.

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

AdcortexClient
------------------

The :class:`adcortex.client.AdcortexClient` is used for fetching ads based on user messages without the chat context.

**Constructor:**

.. code-block:: python

    AdcortexClient(
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
    )

- **session_info**: Instance of :class:`adcortex.types.SessionInfo` with session, character, user, and platform details.
- **context_template**: A template string to format ad context. Default is an empty string.
- **api_key**: ADCORTEX API key. If not provided, it is loaded from the environment variable.

**Key Methods:**

- ``_generate_payload(messages: List[Message]) -> dict``  
  Prepares the payload for the ad request based on the provided messages.

- ``fetch_ad(messages: List[Message]) -> Ad``  
  Sends a request to fetch an ad based on the provided messages and returns an instance of :class:`adcortex.types.Ad`.

- ``generate_context(ad: Ad) -> str``  
  Generates a context string for the provided ad using the context template.

API Reference
=============

This section describes the main classes and methods of the ADCortex Chat Client library.

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   adcortex.chat_client.AdcortexChatClient
   adcortex.async_chat_client.AsyncAdcortexChatClient
   adcortex.types
   adcortex.state

Detailed documentation for the chat clients and types is provided below.

AdcortexChatClient
------------------

The :class:`adcortex.chat_client.AdcortexChatClient` is the primary interface for integrating chat-based advertising into your application. It provides synchronous message processing with built-in error handling and circuit breaker pattern.

**Constructor:**

.. code-block:: python

    AdcortexChatClient(
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        timeout: Optional[int] = 3,
        log_level: Optional[int] = logging.ERROR,
        disable_logging: bool = False,
        max_queue_size: int = 100,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: int = 120,
    )

- **session_info**: Instance of :class:`adcortex.types.SessionInfo` with session, character, user, and platform details.
- **context_template**: A template string to format ad context. Default is `"Here is a product the user might like: {ad_title} - {ad_description}: here is a sample way to present it: {placement_template}"`.
- **api_key**: ADCORTEX API key. If not provided, it is loaded from the environment variable.
- **timeout**: Request timeout in seconds. Default is 3.
- **log_level**: Logging level. Default is ERROR.
- **disable_logging**: Whether to disable logging. Default is False.
- **max_queue_size**: Maximum number of messages in the queue. Default is 100.
- **circuit_breaker_threshold**: Number of consecutive errors before opening circuit breaker. Default is 5.
- **circuit_breaker_timeout**: Time in seconds before circuit breaker resets. Default is 120.

**Key Methods:**

- ``__call__(role: Role, content: str) -> None``  
  Adds a message to the queue and processes it if conditions are met. Only processes messages when:
  - The client is in IDLE state
  - The message role is USER
  - The circuit breaker is closed
  - The queue is not full

- ``create_context() -> str``  
  Generates a context string using the latest fetched ad.

- ``get_latest_ad() -> Optional[Ad]``  
  Gets the latest ad and clears it from memory.

- ``get_state() -> ClientState``  
  Gets the current client state (IDLE or PROCESSING).

- ``is_healthy() -> bool``  
  Checks if the client is in a healthy state. Returns False if:
  - The circuit breaker is open
  - The message queue is full

**Circuit Breaker Pattern:**

The client implements a circuit breaker pattern to prevent cascading failures. The circuit breaker:

1. Opens when the error count exceeds the threshold
2. Stays open for the specified timeout period
3. Automatically resets after the timeout
4. Records errors for:
   - API timeouts
   - Request failures
   - Invalid response formats
   - Unexpected errors

AsyncAdcortexChatClient
----------------------

The :class:`adcortex.async_chat_client.AsyncAdcortexChatClient` provides an asynchronous interface for chat-based advertising with the same features as the synchronous client.

**Constructor:**

.. code-block:: python

    AsyncAdcortexChatClient(
        session_info: SessionInfo,
        context_template: Optional[str] = DEFAULT_CONTEXT_TEMPLATE,
        api_key: Optional[str] = None,
        timeout: Optional[int] = 3,
        log_level: Optional[int] = logging.ERROR,
        disable_logging: bool = False,
        max_queue_size: int = 100,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: int = 120,
    )

Parameters are the same as the synchronous client.

**Key Methods:**

- ``async __call__(role: Role, content: str) -> None``  
  Asynchronously adds a message to the queue and processes it if conditions are met.

Other methods are the same as the synchronous client.

**Additional Features:**

- Asynchronous message processing with task management
- Automatic task cancellation on errors
- Non-blocking queue operations
- Concurrent request handling

State Management
---------------

The client maintains several states:

1. **ClientState**:
   - IDLE: Ready to process messages
   - PROCESSING: Currently processing messages

2. **Circuit Breaker State**:
   - Closed: Normal operation
   - Open: Temporarily disabled due to errors
   - Half-Open: Testing if service has recovered

3. **Queue State**:
   - FIFO (First In, First Out) message processing
   - Automatic removal of oldest messages when full
   - Batch processing of messages

Error Handling
-------------

The client implements comprehensive error handling:

1. **Automatic Retries**:
   - 3 attempts for network-related errors
   - Exponential backoff between retries
   - Configurable timeout periods

2. **Error Types Handled**:
   - Network timeouts
   - API request failures
   - Invalid response formats
   - Validation errors
   - Unexpected exceptions

3. **Circuit Breaker Integration**:
   - Error counting and threshold monitoring
   - Automatic service recovery
   - Configurable error thresholds and timeouts

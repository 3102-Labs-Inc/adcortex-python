Data Types
==========

This document describes the types defined in the ``adcortex.types`` module used by the ADCortex API client.

Enums
-----

Gender
~~~~~~

.. py:class:: Gender(str, Enum)
   :noindex:

   **Enumeration of possible gender values.**

   **Members:**
   
   - **male**: Represents the male gender.
   - **female**: Represents the female gender.
   - **other**: Represents any gender not covered by male or female.

Role
~~~~

.. py:class:: Role(str, Enum)
   :noindex:

   **Enumeration of possible roles for message senders.**

   **Members:**
   
   - **user**: Indicates that the message sender is a user.
   - **ai**: Indicates that the message sender is an AI.

Interest
~~~~~~~~

.. py:class:: Interest(str, Enum)
   :noindex:

   **Enumeration of user interests.**

   **Members:**
   
   - **flirting**: Indicates an interest in flirting.
   - **gaming**: Indicates an interest in gaming.
   - **sports**: Indicates an interest in sports.
   - **music**: Indicates an interest in music.
   - **travel**: Indicates an interest in travel.
   - **technology**: Indicates an interest in technology.
   - **art**: Indicates an interest in art.
   - **cooking**: Indicates an interest in cooking.
   - **all**: Represents all interests.

Language
~~~~~~~~

.. py:class:: Language(Enum)
   :noindex:

   **Enumeration of supported languages.**

   **Members:**
   
   - Various language codes (e.g., **en**, **es**, **fr**, etc.)

Classes
-------

UserInfo
~~~~~~~~

.. py:class:: UserInfo(BaseModel)
   :noindex:

   **Stores user information for ADCortex API.**

   **Attributes:**
   
   - **user_id (str)**: Unique identifier for the user.
   - **age (int)**: User's age.
   - **gender (Gender)**: User's gender.
   - **location (str)**: User's location (ISO 3166-1 alpha-2 code).
   - **language (str)**: Preferred language (must be one of the Language enum values).
   - **interests (List[Interest])**: A list of user's interests.

   **Validators:**
   
   - **validate_age(value)**: Validates that age is greater than 0.
   - **validate_gender(value)**: Validates that gender is a valid Gender enum value.
   - **validate_language(value)**: Validates that language is a valid Language enum value.
   - **validate_interests(value)**: Validates that interests are valid Interest enum values.
   - **validate_country(value)**: Validates that location is a valid ISO 3166-1 alpha-2 country code.

Platform
~~~~~~~~

.. py:class:: Platform(BaseModel)
   :noindex:

   **Contains platform-related metadata.**

   **Attributes:**
   
   - **name (str)**: Name of the platform.
   - **varient (str)**: Variant for experimentation. Default is "default".

SessionInfo
~~~~~~~~~~~

.. py:class:: SessionInfo(BaseModel)
   :noindex:

   **Stores session details including user and platform information.**

   **Attributes:**
   
   - **session_id (str)**: Unique identifier for the session.
   - **character_name (str)**: Name of the character (assistant).
   - **character_metadata (str)**: Additional metadata for the character as a string.
   - **user_info (UserInfo)**: User information.
   - **platform (Platform)**: Platform details.

Message
~~~~~~~

.. py:class:: Message(BaseModel)
   :noindex:

   **Represents a single message in a conversation.**

   **Attributes:**
   
   - **role (Role)**: The role of the message sender.
   - **content (str)**: The content of the message.
   - **timestamp (float)**: The timestamp of when the message was created.

Ad
~~

.. py:class:: Ad(BaseModel)
   :noindex:

   **Represents an advertisement fetched via the ADCortex API.**

   **Attributes:**
   
   - **ad_title (str)**: Title of the advertisement.
   - **ad_description (str)**: Description of the advertisement.
   - **placement_template (str)**: Template used for ad placement.
   - **link (str)**: URL link to the advertised product or service.

AdResponse
~~~~~~~~~

.. py:class:: AdResponse(BaseModel)
   :noindex:

   **Schema for validating ADCortex API responses.**

   **Attributes:**
   
   - **ads (List[Ad])**: List of ads returned by the API.

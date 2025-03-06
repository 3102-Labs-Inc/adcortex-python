Data Types
==========

The ADCortex Chat Client library uses several data classes and enumerated types defined in the
``adcortex.types`` module. This section provides an overview of these classes, their attributes, and the
possible values for the enumerations.

Module Documentation
--------------------

.. automodule:: adcortex.types
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

UserInfo
~~~~~~~~

.. autoclass:: adcortex.types.UserInfo
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **user_id (str):** Unique identifier for the user.
   - **age (int):** User's age.
   - **gender (Gender):** User's gender.
   - **location (str):** ISO 3166-1 alpha-2 code representing the user's location.
   - **language (str):** ISO 639-1 code for the user's preferred language.
   - **interests (List[Interest]):** List of the user's interests.

Platform
~~~~~~~~

.. autoclass:: adcortex.types.Platform
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **name (str):** Name of the platform.
   - **version (str):** Version of the platform.

SessionInfo
~~~~~~~~~~~

.. autoclass:: adcortex.types.SessionInfo
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **session_id (str):** Unique identifier for the session.
   - **character_name (str):** Name of the character (assistant).
   - **character_metadata (Dict[str, Any]):** Additional metadata for the character.
   - **user_info (UserInfo):** User information.
   - **platform (Platform):** Platform details.

Message
~~~~~~~

.. autoclass:: adcortex.types.Message
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **role (Role):** The role of the message sender (either `user` or `ai`).
   - **content (str):** The content of the message.

Ad
~~

.. autoclass:: adcortex.types.Ad
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **idx (int):** Identifier for the advertisement.
   - **ad_title (str):** Title of the advertisement.
   - **ad_description (str):** Description of the advertisement.
   - **placement_template (str):** Template used for ad placement.
   - **link (str):** URL link to the advertised product or service.

Enumerations
============

Gender
~~~~~~

.. autoclass:: adcortex.types.Gender
   :members:
   :undoc-members:
   :show-inheritance:

Role
~~~~

.. autoclass:: adcortex.types.Role
   :members:
   :undoc-members:
   :show-inheritance:

Interest
~~~~~~~~

.. autoclass:: adcortex.types.Interest
   :members:
   :undoc-members:
   :show-inheritance:

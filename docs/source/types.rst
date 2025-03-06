Data Types
==========

The ADCortex Chat Client library uses several data classes defined in the ``adcortex.types`` module. This section provides an overview of these classes.

UserInfo
--------

.. autoclass:: adcortex.types.UserInfo
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **user_id (str)**: Unique identifier for the user.
   - **age (int)**: User's age.
   - **gender (Gender)**: User's gender.
     - Possible values:
       - `Gender.male`
       - `Gender.female`
       - `Gender.other`
   - **location (str)**: User's location represented as an ISO 3166-1 alpha-2 code (e.g., "US" for the United States).
   - **language (str)**: Preferred language represented as an ISO 639-1 code (e.g., "en" for English).
   - **interests (List[Interest])**: A list of user's interests.
     - Possible values:
       - `Interest.flirting`
       - `Interest.gaming`
       - `Interest.sports`
       - `Interest.music`
       - `Interest.travel`
       - `Interest.technology`
       - `Interest.art`
       - `Interest.cooking`
       - `Interest.all` (indicates all interests can be recommended)

Platform
--------

.. autoclass:: adcortex.types.Platform
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **name (str)**: Name of the platform.
   - **version (str)**: Version of the platform.

SessionInfo
-----------

.. autoclass:: adcortex.types.SessionInfo
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **session_id (str)**: Unique identifier for the session.
   - **character_name (str)**: Name of the character (assistant).
   - **character_metadata (Dict[str, Any])**: Additional metadata for the character.
   - **user_info (UserInfo)**: User information.
   - **platform (Platform)**: Platform details.

Message
-------

.. autoclass:: adcortex.types.Message
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **role (Role)**: The role of the message sender.
     - Possible values:
       - `Role.user`
       - `Role.ai`
   - **content (str)**: The content of the message.

Ad
--

.. autoclass:: adcortex.types.Ad
   :members:
   :undoc-members:
   :show-inheritance:

   **Attributes:**
   - **idx (int)**: Identifier for the ad.
   - **ad_title (str)**: Title of the advertisement.
   - **ad_description (str)**: Description of the advertisement.
   - **placement_template (str)**: Template used for ad placement.
   - **link (str)**: URL link to the advertised product or service.

Enums
=====

Gender
------

.. rubric:: Possible values:
   - `male`
   - `female`
   - `other`

Role
----

.. rubric:: Possible values:
   - `user`
   - `ai`

Interest
--------

.. rubric:: Possible values:
   - `flirting`
   - `gaming`
   - `sports`
   - `music`
   - `travel`
   - `technology`
   - `art`
   - `cooking`
   - `all`  # Option for all interests

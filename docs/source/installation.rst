Installation
============

To install the ADCortex Chat Client library, follow these steps:

1. **Install the Package**

   .. code-block:: bash

      pip install adcortex

2. **Set Up Environment Variables**

   Create a ``.env`` file in the project root and add your ADCORTEX_API_KEY:

   .. code-block:: none

      ADCORTEX_API_KEY=your_api_key_here

3. **Required Dependencies**

   The package requires the following dependencies:
   
   - Python 3.8+
   - httpx
   - pydantic
   - python-dotenv
   - tenacity
   - pycountry

   These will be installed automatically when installing the package.

4. **Optional Dependencies**

   For development and testing:
   
   - pytest
   - pytest-asyncio
   - pytest-cov
   - black
   - isort
   - mypy

After these steps, the library is ready to use.

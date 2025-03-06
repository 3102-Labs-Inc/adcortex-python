# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the src folder to sys.path so that Sphinx can locate your package
sys.path.insert(0, os.path.abspath('../../src'))

# --- Extract project metadata from pyproject.toml ---

# Attempt to import tomllib (Python 3.11+) and fall back to the toml package if needed.
try:
    import tomllib  # Available in Python 3.11+
except ImportError:
    import toml as tomllib  # For older Python versions: install with `pip install toml`

# Determine the absolute path to the pyproject.toml file (assumed to be in the project root)
pyproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pyproject.toml'))

with open(pyproject_path, "rb") as f:
    pyproject_data = tomllib.load(f)

# Extract project metadata according to PEP 621
project_info = pyproject_data.get("project", {})

project = project_info.get("name", "adcortex-python")
release = project_info.get("version", "0.0.0")

# Extract author information: expecting a list of authors, each being a table with a 'name' key.
authors = project_info.get("authors", [])
author = authors[0].get("name", "3102labs") if authors else "3102labs"
copyright = '2025, 3102labs'
# --- End of metadata extraction ---

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# Set autodoc default options to include all members and show inheritance details
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']




import os
import sys

# Add the src folder to sys.path so that Sphinx can locate your package
sys.path.insert(0, os.path.abspath("../../src"))

# --- Extract project metadata from pyproject.toml ---

# Try to import tomllib (Python 3.11+) and set the appropriate open mode.
try:
    import tomllib  # Available in Python 3.11+

    open_mode = "rb"
except ImportError:
    import toml as tomllib  # Fallback for older Python versions: install with `pip install toml`

    open_mode = "r"

pyproject_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../pyproject.toml")
)

if open_mode == "rb":
    with open(pyproject_path, open_mode) as f:
        pyproject_data = tomllib.load(f)
else:
    with open(pyproject_path, open_mode, encoding="utf-8") as f:
        pyproject_data = tomllib.load(f)

# Extract project metadata according to PEP 621
project_info = pyproject_data.get("project", {})

project = project_info.get("name", "adcortex")
release = project_info.get("version", "0.0.0")

# Extract author information: expecting a list of authors, each being a table with a 'name' key.
authors = project_info.get("authors", [])
author = authors[0].get("name", "3102labs") if authors else "3102labs"
copyright = "2025, 3102labs"
# --- End of metadata extraction ---

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

# Set autodoc default options to include all members and show inheritance details
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]

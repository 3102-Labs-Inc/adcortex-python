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
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# Set autodoc default options to include all members and show inheritance details
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__call__",
}

# Pygments configuration
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# Syntax highlighting options
highlight_language = "python3"
highlight_options = {
    "stripall": True,
    "stripnl": True,
    "startinline": True,
}

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]

# Theme options
html_theme_options = {
    "navigation_with_keys": True,
    "source_repository": None,
    "source_branch": None,
    "source_directory": None,
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/3102labs/adcortex-python",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

# Add custom CSS
html_css_files = [
    "custom.css",
]

# Add custom JavaScript
html_js_files = [
    "custom.js",
]

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "httpx": ("https://www.python-httpx.org/", None),
}

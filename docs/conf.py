from pathlib import Path
import sys
import tomllib

PROJECT_ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

metadata = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text())["project"]

project = "rangeslib"
author = "Aaryan Banerjee"
release = metadata["version"]

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

html_theme = "alabaster"
html_title = "rangeslib documentation"
exclude_patterns = ["_build"]

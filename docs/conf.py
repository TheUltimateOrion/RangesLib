from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

project = "rangeslib"
author = "RangesLib contributors"
release = "0.2.0"

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

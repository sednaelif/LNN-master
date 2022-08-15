# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.


import os
import sys
import sphinx_material  # noqa: F401
import commonmark  # noqa: F401

sys.path.insert(0, os.path.abspath("../../"))

# -- Project information -----------------------------------------------------

project = "Logical Neural Networks"
copyright = "2022, IBM Research"
author = "IBM Research"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "myst_parser",
    "sphinx_material",
]

html_sidebars = {"**": ["globaltoc.html", "localtoc.html", "searchbox.html"]}

html_use_index = True
html_domain_indices = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = list()


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_material"
html_title = "Logical Neural Networks Docs"
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()

html_theme_options = {
    "nav_title": "Logical Neural Networks",
    "color_primary": "blue",
    "color_accent": "cyan",
    "html_minify": False,
    "html_prettify": True,
    "css_minify": True,
    "repo_type": "github",
    "base_url": "https://github.com/ibm/LNN/",
    "repo_url": "https://github.com/ibm/LNN/tree/master",
    "repo_name": "LNN",
    "globaltoc_depth": 2,
    "globaltoc_collapse": True,
    "globaltoc_includehidden": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def docstring(app, what, name, obj, options, lines):
    md = "\n".join(lines)
    ast = commonmark.Parser().parse(md)
    rst = commonmark.ReStructuredTextRenderer().render(ast)
    lines.clear()
    lines += rst.splitlines()


def setup(app):
    app.connect("autodoc-process-docstring", docstring)
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import subprocess
import re
import sys

sys.path.insert(0, os.path.abspath("../python"))


# -- Project information -----------------------------------------------------

project = "Enhanced Enum"
copyright = "2019, Jaakko Moisio"
author = "Jaakko Moisio"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "breathe",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Autodoc configurations
autoclass_content = "both"

# Breathe Configuration
breathe_default_project = "EnhancedEnum"

read_the_docs_build = os.environ.get("READTHEDOCS", None) == "True"

breathe_projects = {}

if read_the_docs_build:
    input_dir = "../cxx/include"
    output_dir = "build"
    with open("Doxyfile.in") as infile:
        doxyfile_contents = infile.read()
    doxyfile_contents = (
        doxyfile_contents.replace("@ENHANCEDENUM_INCLUDE_DIR@", input_dir)
        .replace("@DOXYGEN_OUTPUT_DIR@", output_dir)
        .replace("@CMAKE_PROJECT_NAME@", "")
        .replace("@CMAKE_PROJECT_VERSION@", "")
        .replace("@CMAKE_PROJECT_DESCRIPTION@", "")
    )
    with open("Doxyfile", "w") as outfile:
        outfile.write(doxyfile_contents)
    subprocess.call("doxygen", shell=True)
    breathe_projects["EnhancedEnum"] = output_dir + "/xml"

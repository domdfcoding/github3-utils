#!/usr/bin/env python3

# This file is managed by 'repo_helper'. Don't edit it directly.

# stdlib
import os
import re
import sys

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(".."))

# this package
from __pkginfo__ import __version__

github_username = "domdfcoding"
github_repository = "github3-utils"
author = "Dominic Davis-Foster"
project = "github3-utils"
copyright = "2020-2021 Dominic Davis-Foster"
language = "en"
package_root = "github3_utils"
extensions = [
		"sphinx_toolbox",
		"sphinx_toolbox.more_autodoc",
		"sphinx_toolbox.more_autosummary",
		"sphinx_toolbox.documentation_summary",
		"sphinx_toolbox.tweaks.param_dash",
		"sphinx_toolbox.tweaks.latex_toc",
		"sphinx.ext.intersphinx",
		"sphinx.ext.mathjax",
		"sphinxcontrib.httpdomain",
		"sphinxcontrib.extras_require",
		"sphinx.ext.todo",
		"sphinxemoji.sphinxemoji",
		"notfound.extension",
		"sphinx_copybutton",
		"sphinxcontrib.default_values",
		"sphinxcontrib.toctree_plus",
		"sphinx_debuginfo",
		"seed_intersphinx_mapping",
		"attr_utils.autoattrs",
		"attr_utils.annotations",
		"sphinx_autofixture",
		]
sphinxemoji_style = "twemoji"
gitstamp_fmt = "%d %b %Y"
templates_path = ["_templates"]
html_static_path = ["_static"]
source_suffix = ".rst"
master_doc = "index"
suppress_warnings = ["image.nonlocal_uri"]
pygments_style = "default"
html_theme = "furo"
html_theme_path = ["../.."]
html_show_sourcelink = True
toctree_plus_types = [
		"class",
		"confval",
		"data",
		"directive",
		"enum",
		"exception",
		"flag",
		"function",
		"method",
		"namedtuple",
		"protocol",
		"role",
		"typeddict",
		]
add_module_names = False
hide_none_rtype = True
all_typevars = True
overloads_location = "bottom"
documentation_summary = "Handy utilities for github3.py"
autodoc_exclude_members = [
		"__dict__",
		"__class__",
		"__dir__",
		"__weakref__",
		"__module__",
		"__annotations__",
		"__orig_bases__",
		"__parameters__",
		"__subclasshook__",
		"__init_subclass__",
		"__attrs_attrs__",
		"__init__",
		"__new__",
		"__getnewargs__",
		"__abstractmethods__",
		"__hash__",
		]

github_url = f"https://github.com/{github_username}/{github_repository}"

rst_prolog = f""".. |pkgname| replace:: github3-utils
.. |pkgname2| replace:: ``github3-utils``
.. |browse_github| replace:: `Browse the GitHub Repository <{github_url}>`__
"""

slug = re.sub(r'\W+', '-', project.lower())
release = version = __version__

todo_include_todos = bool(os.environ.get("SHOW_TODOS", 0))

intersphinx_mapping = {
		"python": ("https://docs.python.org/3/", None),
		"sphinx": ("https://www.sphinx-doc.org/en/stable/", None),
		"github3": ("https://github3py.readthedocs.io/en/master/", None),
		}

html_theme_options = {
		"light_css_variables": {
				"toc-title-font-size": "12pt",
				"toc-font-size": "12pt",
				"admonition-font-size": "12pt",
				},
		"dark_css_variables": {
				"toc-title-font-size": "12pt",
				"toc-font-size": "12pt",
				"admonition-font-size": "12pt",
				},
		}

html_context = {}
htmlhelp_basename = slug

latex_documents = [("index", f'{slug}.tex', project, author, "manual")]
man_pages = [("index", slug, project, [author], 1)]
texinfo_documents = [("index", slug, project, author, slug, project, "Miscellaneous")]

toctree_plus_types = set(toctree_plus_types)

autodoc_default_options = {
		"members": None,  # Include all members (methods).
		"special-members": None,
		"autosummary": None,
		"show-inheritance": None,
		"exclude-members": ','.join(autodoc_exclude_members),
		}

toctree_plus_types.add("fixture")

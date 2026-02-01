# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Bucks'
copyright = '2026, Edga Donk'
author = 'Edga Donk'
release = '0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_copybutton',
    'matplotlib.sphinxext.plot_directive',
    "sphinxext_altair.altairplot",
    'sphinx.ext.mathjax',
    "sphinx.ext.autodoc",
    'sphinx.ext.napoleon',
    "sphinx.ext.autosummary",
    "sphinx_togglebutton",
    "sphinx.ext.autosectionlabel",
    ]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

plot_include_source = False
plot_html_show_source_link = False

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

pygments_style = 'sphinx'
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]

html_theme_options = {
  "show_prev_next": True,
  # search bar options are ‘navbar’ and ‘sidebar’.
  "search_bar_position": "navbar",
  #  "use_edit_page_button": True,

}

html_sidebars = {
    "contributing": ["sidebar-search-bs.html", "custom-template.html"],
    "changelog": [],
}

html_theme_options = {
   "logo": {
      "text": "Big Bucks",
      "image_light": 'bigbenc.png',
      "image_dark": "bigbencneon.png",
   }
}

html_favicon = '_static/ben1.ico'

# For the altairplot extension
altairplot_links = {"editor": True, "source": True, "export": True}

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

smartquotes = False

rst_prolog = f"""
.. role:: AL
    :class: keys
"""





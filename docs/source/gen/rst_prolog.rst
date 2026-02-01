===========
Sphinx Role
===========

Using a combination of information from
`Sphinx substitutions <https://bylr.info/articles/2022/09/30/til-sphinx-substitutions/>`_
and `Stackoverflow <https://stackoverflow.com/questions/49530807/custom-font-with-css-not-work-in-sphinx-project>`_, 
we can create a custom section for part of our text. This only works for one instance, which
can be used as often as you like.

Sphinx  Setup
=============

Assuming we have a modern Sphinx layout, but it also works on the older layout::

   Application
      ├──docs
      │     ├──build
      │     ├──source
      │     │     ├──_static
      │     │     │     ├──css
      │     │     │     └──fonts
      │     │     ├──_templates
      │     │     ├──app files
      │     │     ├──conf.py
      │     │     └──index-rst
      │     │
      │     ├──make.bat
      │     └──Makefile
      │    
      └──README.md
      
This shows a simplified modern layout - we are mostly involved in the *source*
folder - use the *css* folder to store our scripts and the *fonts* folder to store
custom fonts. *conf.py* is the central file where any changes to the configuration 
and methods are made. 

Customising Parts of Sphinx
============================

Normally all the fonts and sizes are handled by the sphinx theme. Each part
of sphinx is covered and we have no normal methods to change a part of the text apart
from standard sphinx methods - in our case using rst.

This method allows us to use a font using standard css rules within our custom style
file, *custom.css* found within the *css* folder::

   @font-face {
     font-family: "Kingofthieves";
     src: url((../fonts/Kingofthieves-v6mL.ttf);
   }

The font was in the *fonts* folder and required the relative path between the folders
*css* and *fonts*. This font is now available to custom.css. Now add our instructions
on how it should be rendered::

   .keys {
      font-family: "Kingofthieves";
      font-size: 60px;
      color: #ff073a;
      text-shadow: 0 0 3px #ccff02; 
   }

We are using a class *keys* preceded with a full stop. In this case we want to use our
custom font, with its size, color and text shadow.

Now to make it work *conf.py* must be configured. Ensure that the following two
lines exist in *conf.py*::

   html_static_path = ['_static']
   html_css_files = ['css/custom.css']

All this does is tell *conf.py* where to find our custom style file and its
name. Now to tell *conf.py* what to do::

   rst_prolog = f"""
   .. role:: AL
      :class: keys
   """

We have added an rst role called *AL* and it will use the input from our custom
class *keys*, which *conf.py* knows is in our custom script. All we have to
do is call up *AL* together with the text that requires altering::

   :AL:`Frothy Brew`

Our text is enclosed in single backward pointing inverted commas.

Unfortunately as there is only one *rst_prolog* role we are limited in our
actions. To see this in action :ref:`my-reference-label`.


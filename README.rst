Babel Godot - Thrive plugin
===========================

This is a plugin for `Babel <http://babel.pocoo.org/>`_, the internationalization library, that adds support for scene files from the `Godot game engine <https://godotengine.org/>`_.

Extended specifically for Thrive, including and slightly editing the plugin `pybabel-json <https://github.com/tigrawap/pybabel-json/>`_.

Installation
------------

Install Babel and this plugin::

    pip install Babel Babel-Thrive

Usage
-----

Using a mapping file like this::

    [csharp: **.cs]
    encoding = utf-8

    [godot_scene: **.tscn]
    encoding = utf-8

    [godot_resource: **.tres]
    encoding = utf-8

    [json: **.json]
    encoding = utf-8

you can extract messages to be translated from both your ``.gd`` and ``.tscn`` files using::

    pybabel extract -F babelrc -k LineEdit -k text -k window_title -k dialog_text -k Translate -o messages.pot .

You can then create ``.po`` files from the POT catalog using `Poedit <https://poedit.net/>`_, or online services  such as `Crowdin <https://crowdin.com/>`_, `Transifex <https://www.transifex.com/>`_, or `Weblate <https://weblate.org/>`_.

Developing
----------

requirements-dev.txt contains packages that help with local development.


To install for local testing::

    pip install . --user


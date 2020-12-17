# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='Babel-Thrive',
    version='1.7',
    description='Plugin for Babel to support Godot scene files (.tscn) extended for Thrive',
    author='Remi Rampin (original), Nicolas Viseur and Henri Hyyryläinen (fork)',
    author_email='westtunger@gmail.com',
    license='BSD',
    url='https://github.com/Revolutionary-Games/pybabel-godot-thrive',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    py_modules=['babel_godot', 'json_extractor', 'csharp_extractor'],

    entry_points="""
    [babel.extractors]
    godot_scene = babel_godot:extract_godot_scene
    godot_resource = babel_godot:extract_godot_resource
    json = json_extractor:extract_json
    csharp = csharp_extractor:extract_csharp
    """
)

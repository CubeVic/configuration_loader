Welcome to ConfigLoader's documentation!
====================================

ConfigLoader is a flexible and extensible configuration loader for Python applications.
It supports multiple configuration formats (YAML, JSON, TOML) and sources (files, environment variables, CLI arguments).

Features
--------

* Multiple configuration formats (YAML, JSON, TOML)
* Environment variable support
* CLI argument integration
* Custom configuration sources
* Pydantic validation
* Caching mechanism
* Extensible architecture

Installation
-----------

.. code-block:: bash

   pip install configloader

Quick Start
----------

.. code-block:: python

   from configloader import ConfigLoader

   # Basic usage
   loader = ConfigLoader(config_file_name="config.yaml")
   config = loader.load_config()

   # With environment variables
   loader = ConfigLoader(
       config_file_name="config.yaml",
       env_prefix="APP_"
   )

   # With validation
   from pydantic import BaseModel

   class Config(BaseModel):
       name: str
       version: str
       debug: bool = False

   loader = ConfigLoader(
       config_file_name="config.yaml",
       config_model=Config
   )

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
   api
   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 
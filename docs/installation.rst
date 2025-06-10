Installation
============

Requirements
------------

wave_view requires Python 3.8 or later and the following dependencies:

* plotly >= 5.0.0
* numpy >= 1.20.0
* PyYAML >= 6.0
* spicelib >= 1.0.0

Basic Installation
------------------

Install wave_view from PyPI using pip:

.. code-block:: bash

   pip install wave_view

Development Installation
------------------------

If you want to contribute to wave_view or need the latest development version:

.. code-block:: bash

   git clone https://github.com/yourusername/wave_view.git
   cd wave_view
   pip install -e ".[dev]"

This installs wave_view in development mode with additional dependencies for testing and development.

Optional Dependencies
---------------------

Documentation
~~~~~~~~~~~~~

To build the documentation locally:

.. code-block:: bash

   pip install "wave_view[docs]"

This includes:

* sphinx >= 5.0.0
* sphinx-rtd-theme >= 1.0.0
* myst-parser >= 0.18.0

Jupyter Support
~~~~~~~~~~~~~~~

For enhanced Jupyter notebook support:

.. code-block:: bash

   pip install "wave_view[jupyter]"

This includes:

* ipywidgets >= 8.0.0
* jupyter >= 1.0.0
* jupyterlab >= 3.0.0

Development Tools
~~~~~~~~~~~~~~~~~

For development and testing:

.. code-block:: bash

   pip install "wave_view[dev]"

This includes testing, linting, and formatting tools:

* pytest >= 7.0.0
* pytest-cov >= 4.0.0
* black >= 22.0.0
* isort >= 5.0.0
* flake8 >= 4.0.0
* mypy >= 1.0.0
* pre-commit >= 2.0.0

Verification
------------

To verify your installation, run:

.. code-block:: python

   import wave_view as wv
   print(wv.__version__)

This should print the version number without any errors. 
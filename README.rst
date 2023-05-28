##############
github3-utils
##############

.. start short_desc

**Handy utilities for github3.py**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/github3-utils/latest?logo=read-the-docs
	:target: https://github3-utils.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/github3-utils/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/github3-utils/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/github3-utils/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/github3-utils/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/github3-utils/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/github3-utils/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/github3-utils/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/github3-utils/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/github3-utils/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/github3-utils/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/github3-utils/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/github3-utils/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/github3-utils/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/github3-utils/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/github3-utils/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/github3-utils?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/github3-utils?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/github3-utils
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/github3-utils
	:target: https://pypi.org/project/github3-utils/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/github3-utils?logo=python&logoColor=white
	:target: https://pypi.org/project/github3-utils/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/github3-utils
	:target: https://pypi.org/project/github3-utils/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/github3-utils
	:target: https://pypi.org/project/github3-utils/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/github3-utils?logo=anaconda
	:target: https://anaconda.org/domdfcoding/github3-utils
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/github3-utils?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/github3-utils
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/github3-utils
	:target: https://github.com/domdfcoding/github3-utils/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/github3-utils
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/github3-utils/v0.7.1
	:target: https://github.com/domdfcoding/github3-utils/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/github3-utils
	:target: https://github.com/domdfcoding/github3-utils/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2023
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/github3-utils
	:target: https://pypi.org/project/github3-utils/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``github3-utils`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install github3-utils

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install github3-utils

.. end installation

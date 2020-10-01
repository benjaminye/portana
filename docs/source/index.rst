.. Portana documentation master file, created by
   sphinx-quickstart on Wed Sep 30 21:07:31 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Install Dev Environment
========================
To start a dev environment, make sure you have `Poetry <https://python-poetry.org/>`_ installed. Then run:

| ``git clone https://github.com/benjaminye/portana.git``
| ``cd portana``
| ``poetry install``


Run Demo
========
First ``cd`` into poetry's virtual environment directory. You can find it via: ``poetry show -v``

on Unix, run: ``source venv-name/Scripts/activate``

on Windows, run (using Powershell): ``./venv-name/Scripts/Activate.ps1``

then, run ``ipython kernel install --name "portana" --user``



Portana Documentation
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Portana Abstracts
************************
.. automodule:: portana.abstracts.data
   :members:
   
.. automodule:: portana.abstracts.timeseries
   :members:

.. automodule:: portana.abstracts.analyzer
   :members:

Portana Data
************************
.. automodule:: portana.data.simulated
   :members:

.. automodule:: portana.data.generator
   :members:

Portana Timeseries
************************
.. automodule:: portana.timeseries.analyzerseries
   :members:

.. automodule:: portana.timeseries.simtimeseries
   :members:
   
Portana Analyzer
************************
.. automodule:: portana.analyzer.equity_analyzer
   :members:
   



Indices and tables
*********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

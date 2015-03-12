About
=====

This is a collection of example scripts that makes use of the Python package
PyMC, which is an implementation of Bayesian inference in Python. The scripts
here were adapted from a tutorial given at SciPy 2011 held in Austin, TX, by
Christopher Fonnesbeck (founder of PyMC) and Abie Flaxman. The slides for the
tutorial are located in the Tutorial_Slides folder.

Requirements
============

These scripts require Python and the PyMC and NetworkX packages to be installed. For a
convenient installation of Python, you can download the
[Anaconda Python Distribution](https://store.continuum.io/cshop/anaconda/)
from Continuum Analytics. Anaconda includes the PyMC and NetworkX packages.

Files
=====

./
 ├── CFAST_Model            -  Contains the CFAST model executable and holds
 |                                 the temporary CFAST case files when running
 |                                 the CFAST examples.
 |
 ├──├ Example Cases         -  Examples using PyMC in fire scenarios.
 |  |
 |  ├── */Experimental_Data -  Experimental data to be read in by the scripts.
 |  |
 |  ├── */Figures           -  Output figures and plots will be written to
 |  |                              this folder.
 |  |
 |  ├── */PyMC_Output_Files -  Output from PyMC cases that require longer
 |  |                              runtimes (FDS and CFAST).
 |  |
 |  └── */Scripts           -  Contains the example PyMC scripts.
 |
 ├── FDS_Model              -  Contains the FDS model executable and holds the
 |                                 temporary FDS case files when running the
 |                                 FDS examples.
 |
 ├── Scripts_Other          -  Contains Python scripts that demonstrate
 |                                 additional functionality.
 |
 └── Tutorial_Slides        -  Slides from the SciPy 2011 tutorial.

Usage
=====

Run the Run_Case.py Python files in the Scripts directory for each example
case, and check the output in the Figures directory.

The scripts data_*.py, graphics.py, and models.py are called by the example
scripts.

Happy Bayesianing!

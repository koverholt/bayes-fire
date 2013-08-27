=========
= ABOUT =
=========

This is a collection of example scripts that makes use of the Python module
PyMC, which is an implementation of Bayesian inference in Python. The scripts
here were adapted from a tutorial given at SciPy 2011 held in Austin, TX, by
Christopher Fonnesbeck (founder of PyMC) and Abie Flaxman. The slides for the
tutorial are located in the Tutorial_Slides folder.

================
= REQUIREMENTS =
================

These scripts require Python and the PyMC module to be installed. For a
convenient installation of Python, you can download the Continuum Anaconda or
Enthought Canopy Express distributions.

After installing Python, you can use "easy_install pip", then use "pip" to
install PyMC with the command "pip install pymc".

You will also need to install the networkx dependency by using the
command "pip install networkx".

=========
= FILES =
=========

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

=========
= USAGE =
=========

Run the Run_Case.py Python files in the Scripts directory for each example
case, and check the output in the Figures directory.

The scripts data_*.py, graphics.py, and models.py are called by the example
scripts.

Happy Bayesianing!

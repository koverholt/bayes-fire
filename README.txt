Added by Kristopher Overholt
UT Fire Research Group
12/5/2012

=========
= ABOUT =
=========

This is a collection of example scripts that makes use of the Python module PyMC,
which is an implementation of Bayesian inference in Python. The scripts here
were adapted from a tutorial given at SciPy 2011 held in Austin, TX, by
Christopher Fonnesbeck (founder of PyMC) and Abie Flaxman. The slides for the
tutorial are located in the Tutorial_Slides folder.

================
= REQUIREMENTS =
================

These scripts require Python and the PyMC module to be installed.
For a convenient installation of Python, you can download the
EPD Academic or EPD Free Python distribution from Enthought, Inc.
You can "easy_install pip" then use "pip" to install PyMC with the
command "pip install pymc".

You will also need to install the networkx dependency by using the
command "pip install networkx".

=========
= FILES =
=========

./
 ├── CFAST_Files        -  Contains the CFAST model executable and holds the temporary CFAST case files when running the CFAST examples.
 ├── Documentation      -  Folder with this README.txt file and the LICENSE.txt file that originally accompanied the PyMC tutorial scripts.
 ├── Experimental_Data  -  Folder with data to be read in by the scripts.
 ├── FDS_Files          -  Contains the FDS model executable and holds the temporary FDS case files when running the FDS examples.
 ├── FDS_PMMA_Example   -  Contains the results of the FDS MLR example compared to the case in the FDS Validation suite: FDS input and output files as well as a plotting script.
 ├── Figures            -  Output figures and plots will be written to this folder.
 ├── PyMC_Output_Files  -  Output from PyMC cases that require longer runtimes (FDS and CFAST).
 ├── Scripts            -  Contains all of the example PyMC scripts.
 ├── Scripts            -  Contains Python scripts that demonstrate additional functionality.
 └── Tutorial_Slides    -  Slides from the SciPy 2011 tutorial.

=========
= USAGE =
=========

Run the example Python files in the Scripts directory, and check the output in the Figures directory.

The scripts data.py, graphics.py, and models.py are called by the example scripts.

Happy Bayesianing!

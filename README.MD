
# RMIT CAPSTONE PROJECT 
## NORTH EAST WATER

## Context
A program to assist in analysing NEW's industrial energy consumption. Takes `xls` files of interval data, and returns a number of different average load profiles. 

## Scope

Contains a GUI program that will:

- Code to manipulate data into DataFrames.
- Code to plot the data nicely.

This program includes NE Water data from External Sites and within WWTP. 


## VERSION 

Version 1.6.3  
Last Updated: 18MAY20


## OVERVIEW
This program will generate a landing page to direct the user to two seperate GUI's. 

1.  The first GUI will generate a percentage of consumption between two user defined hours. This can be viewed as a graph OR saved as a `xlsx` file with multiple sheets for multiple months. The expected output is a percentage (ie, 0-100%)
    - The output `xlsx` file can be found in `/OUTPUT DATA`
    - Outputs are as follows 
      -  Daily mean per month
      -  Weekly Median per month
      -  Solar generation available for external loads (ie, solar generation LESS WWTP LOAD) - This data is somewhat incomplete.
1.  The second GUI will plot daily and weekly average load profiles for WWTP and external NE Water loads. Various options exist for assisting in the analysis. Currently there is no option to export as a `xlsx` file. The expected output is a graph. 

1.  There are ancillary functions to assist with other data manipulation. These are presented as external to the main `graphy.py` file, and require user input. Theses are as follows. 
    *  `plotty.py` will plot an `xlsx` or `csv` file and plot the existing data to match the format of the main `Graphy.py`. This is useful for data external to `Graphy.py`. This is presented as is, and will require user input, and it will break regularly.  

## How to use

1. Clone the `master` branch. 
  1.   `git clone https://github.com/DOCraven/Graphy.git`.
1. Install Dependencies (if required - `PIP INSTALL [library]`).
1. In Visual Studio Code, open the folder that `Graphy.py` is located in via `CTRL + K + O`.
1. Ensure the `xls` file is in the root folder (ie, same as `Graphy.py`).
1. Run `Graphy.py`. 
   -  either within your IDE (in VS CODE, green triangle in Upper RH corner).
   -  or via the terminal using  `python graphy.py`.
1. Use the included GUI landing page to select the various options.


## Contributing 
1.  Clone the master branch via `git clone https://github.com/DOCraven/Graphy.git`.
1.  Create a new branch either via `git branch [branch-name]` or via the inbuilt GitLens extension (bottom LH corner).
1.  Contribute code.
1.  commit code as necessary via `git commit -m "Message"` or via GitLens Extension.
1.  Push code to new branch via `git push origin [your branch]` or via GitLens Extension (bottom LH Corner).
1.  Request code review (if necessary).
1.  Merge with master when approved.

## Known Issues


- This repo does not place nice with Anaconda. Please use this with a vanilla Python 3.8.x installation.
- There is minimal error checking involved. 
- `WWTP` data is lacking, and thus plotting it will not yield as many results and `EXTERNAL` data. 
- No solar data appended to `WWTP` plotting. 
- Solar data is currently placeholder data, and not site specific data. 


## Dependencies

There are accompanying files required in order for this program to work. These files must be in the root directory. 
-  `GUI_fcn,py`
-  `UTILS_fcn.py`
-  `fcn_Solar_Calculator.py`

There are multiple `xlsx` files in the `/INPUT DATA` folder required for this program to work properly. 
-  `2018_NE_WATER_EXTERNAL_LOAD.xlsx`
-  `2019_NE_WATER_EXTERNAL_LOAD.xlsx`
-  `2020_NE_WATER_EXTERNAL_LOAD.xlsx`
-  `SOLAR_2018_DUMMY.xlsx`
-  `SOLAR_2019_DUMMY.xlsx`
-  `SOLAR_2020_DUMMY.xlsx`
-  `WWTP_2019_DATA.xlsx`
-  `WWTP_2020_DATA.xlsx`


Use `PIP INSTALL [LIBRARY]` to install each dependency. 

-  Python 3.8.x
-  Pandas
-  Cufflinks
-  Plotly 
-  matplotlib
-  PySimpleGUI
-  Numpy
-  xlsxwriter


# RMIT CAPSTONE PROJECT 
## NORTH EAST WATER




## Context
A program to assist in analysing NEW's industrial energy consumption. Takes `xls` files of interval data, and returns a number of different average load profiles. 

## Scope

Contains:

- Code to manipulate data into DataFrames.
- Code to plot the data nicely.

## How to use

1. Clone the `master` branch. 
  1.   `git clone https://github.com/DOCraven/Graphy.git`.
1. Install Dependencies (if required - `PIP INSTALL [library]`).
1. In Visual Studio Code, open the folder that `Graphy.py` is located in via `CTRL + K + O`.
1. Ensure the `xls` file is in the root folder (ie, same as `Graphy.py`).
1. Run `Graphy.py`. 
-  either within your IDE (in VS CODE, green triangle in Upper RH corner).
-  or via the terminal using  `python graphy.py`.
1. Break stuff.


## Contributing 
1.  Clone the master branch via `git clone https://github.com/DOCraven/Graphy.git`.
1.  Create a new branch either via `git branch [branch-name]` or via the inbuilt GitLens extension (bottom LH corner).
1.  Contribute code.
1.  commit code as necessary via `git commit -m "Message"` or via GitLens Extension.
1.  Push code to new branch via `git push origin [your branch]` or via GitLens Extension (bottom LH Corner).
1.  Request code review (if necessary).
1.  Merge with master when approved.

## Known Issues


- The plotter function requires some manual manipulation to get it to plot nicely. 

## Dependencies

Use `PIP INSTALL [LIBRARY]` to install each dependency. 

-  Pandas
-  Cufflinks
-  Plotly 
-  matplotlib

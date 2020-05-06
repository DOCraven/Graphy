### This script will read 30 minutely interval data (supplied via xls) and generate useful outputs. 
# outputs include daily and monthly average, daily Sum, and more to come
# also uses some libraries to make nice interactive graphs for manipulation and interpretation

# THIS PROGRAM REQUIRES ADDITIONAL .py FILES
# - GUI_fcn.py
# - UTILS_fcn.py



### USEFUL STACK EXHANGE AND PANDAS DOCUMENTATION ###

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/resampling.html
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#visualization-scatter-matrix
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases%3E - frequency alias
    

    # https://pandas-docs.github.io/pandas-docs-travis/user_guide/groupby.html # GROUPYBY DATA FOR DOING STUFF ON MULTINDEX STUFF

    # https://stackoverflow.com/a/17001474/13181119
    # https://stackoverflow.com/a/36684166/13181119


    # https://gist.github.com/phobson/8d853ddf23d1d692fe4d#file-sac-regression-ipynb - I THINK THIS IS VERY USEFUL FOR LATER 
    # https://plotly.com/python/cufflinks/ - makes plotting nice and pretty
        # https://github.com/santosjorge/cufflinks



### INPUTS ###
# Plant Load interval data in 30 minute intervals as an .XLS files 
# Solar predictions from PVSyst (resolution TBA) as an .XLS file

### OUTPUTS ###
# interval data split into monthly dataframes
# Pretty graphs 
    # Average Daily Load Profiles for each NEW industrial load
    # Summed daily consumption as a % of max consumption


### libraries

import pandas as pd
import datetime as dt
import cufflinks as cf
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime as dt
from calendar import day_name
import PySimpleGUI as sg

#external explicit function files
from GUI_fcn import Plotter, GUI
from UTILS_fcn import dataJoiner, xlsxReader

### FUNCTIONS ###
def DailyAverage(monthly_data):
    """
    Takes a dataframe of monthly data, and returns an average (mean) day for that month.
    30 days in, 1 day out  
    """
    dailyAverage = [] # Average Day from the input
    columnName = 'Interval End' #name of column that contains Parsed DateTimeObject
    NumberofDataFrames = len(monthly_data)
    for months in  range(0, NumberofDataFrames): # sets each DF to have the correct index
        monthly_data[months] = monthly_data[months].set_index([columnName]) #set the index, as previous DF did not have have an index
        monthly_data[months].index = pd.to_datetime(monthly_data[months].index, unit='s') # some magic to make it not error out - 
        dailyAverage.append(monthly_data[months].groupby([monthly_data[months].index.hour, monthly_data[months].index.minute]).mean()) #sum each days demand, 
        #     returns the mean of the hours over the month 
            # https://stackoverflow.com/a/30580906/13181119
    
    return dailyAverage

def WeeklyAverage(monthly_data):
    """
    Takes a list of dataframes (12x) and returns the average for each week
    30 days in, 7 day out
    as a list of dataframes  
    """
    ## VARS
    fullDateColumnName = 'Interval End' #name of column that contains Parsed DateTimeObject
    WeeklyAverage = []
    day_index = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] #needed for sorting the dataframe into specific days
    
    # Convert monthly datatime into NAME OF DAY and TIME 
    NumberofDataFrames = len(monthly_data)
    
    for months in  range(0, NumberofDataFrames): # iterate through the list of dataframes
        monthly_data[months].reset_index(inplace = True) #remove index to stop it from erroring out with INDEX_ERROR
        monthly_data[months]['TIME'] = monthly_data[months][fullDateColumnName].dt.time #splits time, throws it at the end  
            
        time_temp =  monthly_data[months]['TIME'] #creates new dataframe called TIME for each iteration through the for loop

        monthly_data[months].drop(labels=['TIME'], axis=1,inplace = True) #drops the DATE and TIME from the end of the dataframe
        monthly_data[months].insert(0, 'TIME', time_temp) #inserts TIME at the beginning of the dataframe
            # https://stackoverflow.com/a/25122293/13181119
        
        monthly_data[months]['DAY'] = monthly_data[months][fullDateColumnName].dt.day_name() # get the DAY NAME from datetime object (ie, MONDAY, TUESDAY etc)
            # https://stackoverflow.com/a/30222759/13181119

        dayofweek_temp = monthly_data[months]['DAY'] #new dataframe of day names, to replace DATE with
        
        monthly_data[months].drop(labels=['DAY', fullDateColumnName], axis=1,inplace = True) #drops the DAY column from the end of the dataframe
        monthly_data[months].insert(0, 'DAY', dayofweek_temp) #inserts DAY_OF_WEEK at the beginning of the dataframe
        
    ## DO SOME FANCY MATHS HERE ##
    for months in  range(0, NumberofDataFrames): #iterate through each month
        sorted = monthly_data[months] #temp dataframe to make sorting it easier 
        sorted['DAY'] = pd.Categorical(sorted['DAY'], categories = day_index, ordered = True) #look, some magic happens here, not entirely sure 
            #what the go is. This is the SO reference #https://stackoverflow.com/a/39223389/13181119

        median = sorted.groupby(['DAY', 'TIME']).median() #find the median grouping by DAY and TIME
        WeeklyAverage.append(median) #append to a list of dataframes, and return this to the main function
    
    return WeeklyAverage

def MonthToDaySum(df):
    """
    Sums up the entire DF for the month, returns a total energy consumption for each day of the month, as a % of the highest load in each site
    """
    sampled = [] #empty array
    NumberofDataFrames = len(monthly_data)
    
    for months in  range(0, NumberofDataFrames): # iterate through the list of dataframes
        SUMMED = df[months].resample("1D").sum() #sum each days demand 
        SUMMED = df[months].apply(lambda x: x.div(x.max())) #magic lambda function from Sean, divdes X by the max of X, making it into percentages
        sampled.append(SUMMED) #append to all 
            
    return sampled

def main():
    """ Main fcn"""
    plt.close('all')
    
    ## VARS ##
    cwd = os.getcwd()
    Input_Folder = cwd + '\\INPUT DATA\\'
    startMSG = ('NE WATER DATA ANALYSIS TOOL\n\nThis code takes about a minute to run\nPlease be patient\n\n\n')
    print(startMSG)
        # consumption data
    Interval_data_2018_file_name = Input_Folder + '2018_NE_WATER_EXTERNAL_LOAD.xlsx' #2018 data
    Interval_data_2019_file_name = Input_Folder +  '2019_NE_WATER_EXTERNAL_LOAD.xlsx' #2019 data
    Interval_data_2020_file_name = Input_Folder + '2020_NE_WATER_EXTERNAL_LOAD.xlsx' #2020 data
    
        #solar data - currently dummy data
    Solar_data_2018_file_name = Input_Folder + 'SOLAR_2018_DUMMY.xlsx'
    Solar_data_2019_file_name = Input_Folder + 'SOLAR_2019_DUMMY.xlsx'
    Solar_data_2020_file_name = Input_Folder + 'SOLAR_2020_DUMMY.xlsx'
    
       
    ## STEP 1 - READ XLSX DATA ##
        # Load Data
    FullIntervalData_2018 = xlsxReader(Interval_data_2018_file_name) #split into months, access via indexing 
    print('Read 2018 Data')
    FullIntervalData_2019 = xlsxReader(Interval_data_2019_file_name) #split into months, access via indexing 
    print('Read 2019 Data')
    FullIntervalData_2020 = xlsxReader(Interval_data_2020_file_name) #split into months, access via indexing 
    print('Read 2020 Data')

        #solar data
    FullSolarData_2018 = xlsxReader(Solar_data_2018_file_name)
    FullSolarData_2019 = xlsxReader(Solar_data_2019_file_name)
    FullSolarData_2020 = xlsxReader(Solar_data_2020_file_name)
    
    ## STEP 2 - CONCAT SOLAR DATA ONTO BACK OF RELEVENT YEAR LOAD DATA AND INTERPOLATE NaN if required ##
    FUll_2018_EXTERNAL_DATA = dataJoiner(FullIntervalData_2018, FullSolarData_2018)
    FUll_2019_EXTERNAL_DATA = dataJoiner(FullIntervalData_2019, FullSolarData_2019)
    FUll_2020_EXTERNAL_DATA = dataJoiner(FullIntervalData_2020, FullSolarData_2020)

    ## STEP 3 - CALCULATE DAILY AVERAGE PER MONTH - load data ## - without SOLAR 
    DAILY_MEAN_2018 = DailyAverage(FUll_2018_EXTERNAL_DATA)
    DAILY_MEAN_2019 = DailyAverage(FUll_2019_EXTERNAL_DATA)
    DAILY_MEAN_2020 = DailyAverage(FUll_2020_EXTERNAL_DATA)
    
    ## STEP 4 - CALCULATE WEEKLY AVERAGE PER MONTH ##
    WEEKLY_MEDIAN_2018 = WeeklyAverage(FUll_2018_EXTERNAL_DATA)
    WEEKLY_MEDIAN_2019 = WeeklyAverage(FUll_2019_EXTERNAL_DATA)
    WEEKLY_MEDIAN_2020 = WeeklyAverage(FUll_2020_EXTERNAL_DATA)

    ### STEP N+1 - PLOTTING GRAPHS ###
    GUI(DAILY_MEAN_2018, DAILY_MEAN_2019, DAILY_MEAN_2020, WEEKLY_MEDIAN_2018, WEEKLY_MEDIAN_2019, WEEKLY_MEDIAN_2020)
    
    

    

    return #nothing



### MAIN ###

main()



print('\nCODE \n C\n  O\n   M\n    P\n     L\n      E\n       T\n        E\n         D\n')



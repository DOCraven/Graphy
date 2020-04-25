### This script will read 30 minutely interval data (supplied via xls) and generate useful outputs. 
# outputs include daily and monthly average, daily Sum, and more to come
# also uses some libraries to make nice interactive graphs for manipulation and interpretation




### USEFUL STACK EXHANGE AND PANDAS DOCUMENTATION ###

    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/resampling.html
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#visualization-scatter-matrix

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
import matplotlib.pyplot as plt


### FUNCTIONS ###


def xlsxReader(xls_file_path): 
    """reads a given file (xls_file_path) and returns a list of DataFrames split into months and weeks
    Access said dataframe via indexing
    ie, JAN = 0
        FEB = 1
        ...
        DEC = 11
        WEEK 1 = 0
        WEEK 2 = 1
        ...
        WEEK 52 = 51
    """
    ### STEP 1 -  read the data without index files
    data = pd.read_excel(xls_file_path, parse_dates = True, index_col = None) #reads entire df and parses dates without creating an index
    
    months = [g for n, g in data.groupby(pd.Grouper(key='Interval End',freq='M'))] #splits it into months
        # is a list, so just access each list as an index (ie, JAN = 0, FEB = 1)
        # https://stackoverflow.com/a/49491178/13181119
    


    return months

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
        dailyAverage.append(monthly_data[months].groupby([monthly_data[months].index.hour, monthly_data[months].index.minute]).mean()) #sum each days demand, returns the mean of the hours over the month 
            # https://stackoverflow.com/a/30580906/13181119
    
    dailyAverage[0].to_csv('1 REFERENCE.csv')
    return dailyAverage


def WeeklyAverage(monthly_data):
    """
    Takes a list of dataframes (12x) and returns the average for each week
    30 days in, 7 day out  
    """
    ## VARS
    
    weeks = [] #should have 52 weeks
    columnName = 'Interval End' #name of column that contains Parsed DateTimeObject
    weekIndex = 5 #number of weeks in each month
    
    
    # split into weeks
    NumberofDataFrames = len(monthly_data)
    for months in  range(0, NumberofDataFrames): # sets each dataframe to have the correct index
        WeeksFromMonth = [g for n, g in monthly_data[months].groupby(pd.Grouper(key=columnName,freq='W'))] #splits 1x month into 4x weeks
        weeks.append(WeeksFromMonth) #joins 4x weeks to previous weeks. Week starts on a WED for some reason




    return #nothing


def DailySUM(monthly_data): #BROKEN
    """
    Takes 30 minute interval data over the month, and returns a sum for a each day
    """
    SumofDays = [] #average day 
    columnName = 'Interval End' #name of column that contains Parsed DateTimeObject
    NumberofDataFrames = len(monthly_data) #How many dataframes are in the given list
    for months in  range(0, NumberofDataFrames): # sets each DF to have the correct index
        monthly_data[months] = monthly_data[months].set_index([columnName]) #set the index, as previous DF did not have have an index
        monthly_data[months].index = pd.to_datetime(monthly_data[months].index, unit='s') # some magic to make it not error out - 
        SumofDays.append(monthly_data[months].groupby([monthly_data[months].index.hour, monthly_data[months].index.minute]).sum()) #sum each days demand 
            # https://stackoverflow.com/a/30580906/13181119
    
    return SumofDays

def MonthToDaySum(df): #BROKEN
    """
    Sums up the entire DF for the month, returns a total energy consumption for each day of the month, as a % of the highest load in each site
    """
    sampled = [] #empty array
    for x in range (0, 12): # sets each DF to have the correct index
        SUMMED = df[x].resample("1D").sum() #sum each days demand 
        SUMMED = df[x].apply(lambda x: x.div(x.max())) #magic lambda function from Sean, divdes X by the max of X, making it into percentages
        sampled.append(SUMMED) #append to all 
            
    return sampled

def Plotter(df, TITLE = 'DAILY MEAN', X_LABEL = 'Time', Y_LABEL = 'kWh', PLOTTYPE = 'Subplot'): #this is where things are plotted, will require _some_ manual manipulation until I make it nicer
    """ Plots the given dataframe using cufflinks
    Will require manual manipulation
    """
    ## determing the rows/columns for subplots, change this to output for your screen
    # for portrait screens, 17x2 is best
    # for landscape screens, 2x17 is best
    rows = 17
    columns = 2
 
    #individual plot
    
    # plotting types
    if PLOTTYPE == 'Subplot':
        fig = df.iplot(asFigure=True, subplots=True, shape=(rows, columns), shared_xaxes=True, fill=True, xTitle = X_LABEL, yTitle = Y_LABEL, title = TITLE) #17 2 is best for portrait monitors, 4 9 is best for landscape monitors
    #nice looking individual plot
    elif PLOTTYPE == 'Individual':
        fig = df.iplot(asFigure=True, xTitle=X_LABEL, yTitle=Y_LABEL, title=TITLE)
    elif PLOTTYPE == 'Bar':
        fig = df.iplot(asFigure=True, xTitle=X_LABEL, yTitle=Y_LABEL, title=TITLE, kind = 'bar')
    
    else:
        print('Incorrect Plot Type')


    fig.show()

    return #nothing

    

def main():
    """ Main fcn"""
    plt.close('all')
    ### STEP 1 - read all xlsx and save as monthly df
        ## VARS
    Interval_data_2019_file_name = 'Large Market Interval Data - March 01 2018- Feb 29 2019.xls' #2018/19 data
    # Interval_data_2020_file_name = 'Large Market Interval Data - March 01 2019 -March 01 2020.xls' #2019/20 data
    
        ## READING XLS, change to pick which year
    FullIntervalData_2019 = xlsxReader(Interval_data_2019_file_name) #split into months, access via indexing 
    # FullIntervalData_2020 = xlsxReader(Interval_data_2020_file_name) #split into months, access via indexing 
    
    
            ### STEP 2 - Playing with the data

    
    ## DAILY AVERAGE PER MONTH ##
    # DAILY_MEAN_2019 = DailyAverage(FullIntervalData_2019)
    # DAILY_MEAN_2020 = DailyAverage(FullIntervalData_2020)

    ## WEEKLY AVERAGE PER MONTH ##

    WeeklyAverage(FullIntervalData_2019)
   
    
    
    
    ### PLOTTING NICE GRAPHS ###
    
    month = 1 # to plot a specific month, (JAN = 0, FEB = 1 .... DEC = 11)
    PLOT_TITLE_A = 'FEB DAILY MEAN' #change this to match the month 
    PLOT_TITLE_B = 'FEB TEST WEEKLY MEAN'
    # axis labels
    x_label = 'Time'
    y_label = 'kWh'

    plot_type = 'Individual'
        #plot types
        # 'Subplot'
        # 'Individual'
        # 'bar'

    #call different plotter functions to plot different types of plots for different data
    #TODO: Make the plotter functions more universal
    
    #2019
    # Plotter(DAILY_MEAN_2019[month], TITLE = PLOT_TITLE_A, PLOTTYPE = plot_type, X_LABEL = x_label, Y_LABEL = y_label) #daily average
    # Plotter(TEST[month], TITLE = PLOT_TITLE_B, PLOTTYPE = plot_type, X_LABEL = x_label, Y_LABEL = y_label) #daily average

    return #nothing



### MAIN ###

main()



print('CODE \n C\n  O\n   M\n    P\n     L\n      E\n       T\n        E\n         D\n')



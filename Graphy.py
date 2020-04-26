### This script will read 30 minutely interval data (supplied via xls) and generate useful outputs. 
# outputs include daily and monthly average, daily Sum, and more to come
# also uses some libraries to make nice interactive graphs for manipulation and interpretation




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
import matplotlib.pyplot as plt
import datetime as dt
from calendar import day_name
import PySimpleGUI as sg



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
    as a list of dataframes  
    """
    ## NOTES ##
    # using NEW data, the year starts in March, thus 
    # MAR = 0
    # APR = 1
    # MAY = 2
    # JUN = 3
    # JUL = 4
    # AUG = 5
    # SEP = 6
    # OCT = 7
    # NOV = 8
    # DEC = 9
    # JAN = 10
    # FEB = 11

    ## VARS
    
   
    fullDateColumnName = 'Interval End' #name of column that contains Parsed DateTimeObject
    WeeklyAverage = []
    day_index = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] #needed for sorting the dataframe into specific days
    # Convert monthly datatime into NAME OF DAY and TIME 
    NumberofDataFrames = len(monthly_data)
    # NumberofDataFrames = 2 #for testing 
    for months in  range(0, NumberofDataFrames): # iterate through the list of dataframes
        #convert datetime object into individual date and time columns
        monthly_data[months]['TIME'] = monthly_data[months][fullDateColumnName].dt.time #splits time, throws it at the end  
            ### SOMETIMES ERRORS OUT HERE FOR SOME REASON ###
        
        #create temp holding dataframes so they can be inserted into the front of the dataframe
        time_temp =  monthly_data[months]['TIME'] #creates new dataframe called TIME

        # move the DATE and TIME columns to the front
        monthly_data[months].drop(labels=['TIME'], axis=1,inplace = True) #drops the DATE and TIME from the end of the dataframe
        monthly_data[months].insert(0, 'TIME', time_temp) #inserts TIME at the beginning of the dataframe
       
            # https://stackoverflow.com/a/25122293/13181119
        
        # get the DAY NAME from datetime object
        monthly_data[months]['DAY'] = monthly_data[months][fullDateColumnName].dt.day_name()
            # https://stackoverflow.com/a/30222759/13181119
        dayofweek_temp = monthly_data[months]['DAY'] #new dataframe of day names, to replace DATE with
        monthly_data[months].drop(labels=['DAY', fullDateColumnName], axis=1,inplace = True) #drops the DAY column from the end of the dataframe
        monthly_data[months].insert(0, 'DAY', dayofweek_temp) #inserts DAY_OF_WEEK at the beginning of the dataframe
        # monthly_data[months].set_index(['DAY', 'TIME'], inplace = True) #create a multi index for future things - breaks next bit of function

    ## DO SOME FANCY MATHS HERE ##
    for months in  range(0, NumberofDataFrames): #iterate through each month
        sorted = monthly_data[months] #temp dataframe to make sorting it easier 
        sorted['DAY'] = pd.Categorical(sorted['DAY'], categories = day_index, ordered = True) #look, some magic happens here, not entirely sure 
            #what the go is. This is the SO reference #https://stackoverflow.com/a/39223389/13181119

        median = sorted.groupby(['DAY', 'TIME']).median() #find the median grouping by DAY and TIME
        WeeklyAverage.append(median) #append to a list of dataframes, and return this to the main function
    
    
    # WeeklyAverage[0].to_csv('Updated Median.csv') #FOR TESTING
    return WeeklyAverage

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

def GUI(DAILY_MEAN_2019 = None, DAILY_MEAN_2020 = None, WEEKLY_MEDIAN_2019 = None, WEEKLY_MEDIAN_2020 = None): 
    """ a simple GUI to make plotting easier
    """
    ## VARS
    Months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    Year = ('2019', '2020')
    Location = ('WWTP', "External NEW Plants")
    Interval = ('Daily', 'Weekly')
    Plot = ('Subplot', 'Individual')
    NE_WATER_MONTHS = {10: 'JAN', 11: 'FEB', 0: 'MAR', 1: 'APR', 2: 'MAY', 3: 'JUN', 4: 'JUL', 5: 'AUG', 6: 'SEP', 7: 'OCT', 8: 'NOV', 9: 'DEC'}
    plottype = location = interval = month = year = None #so scope doesnt screw me. Could use a global var, but this is less typing

    #determine the layout
    layout = [  [sg.Text('Pick a month to Plot')],
            [sg.Listbox(Location, size=(20, len(Location)), key='Location')],
            [sg.Listbox(Year, size=(20, len(Year)), key='Year')],
            [sg.Listbox(Months, size=(20, len(Months)), key='Month')],
            [sg.Listbox(Interval, size=(20, len(Interval)), key='Interval')],
            [sg.Listbox(Plot, size=(20, len(Plot)), key='Plot Type')],
            [sg.Button('Plot')]  ]

    window = sg.Window('NEW GRAPHY', layout) #open the window

    while True:               # so the window is peristent
        event, values = window.read() #keep waiting for a user input
        if event is None:
            break
        if event == 'Plot': #ie, plot button is pushed, so execute
            
            if values['Location']: #determine the location 
                selectedLocation = values['Location']
                #do location logic
                if selectedLocation == ['WWTP']: 
                    location = 'Wodonga Water Treatment Plant '
                elif selectedLocation == ['External NEW Plants']:
                    location = 'External '

            if values['Interval']: #determine the interval 
                selectedInterval = values['Interval']
                #do location logic
                if selectedInterval == ['Daily']: 
                    interval = 'Daily'
                elif selectedInterval == ['Weekly']:
                    interval = 'Weekly'
            
            if values['Plot Type']: #determine the Plot Type 
                selectedPlot = values['Plot Type']
                #do location logic
                if selectedPlot == ['Subplot']: 
                    plottype = 'Subplot'
                elif selectedPlot == ['Individual']:
                    plottype = 'Individual'
                    
            #do month logic
            ## NEW DATA MONTH ORDERING (ie, JAN = 10, FEB = 11, MAR = 0)
            
            if values['Month']:    # Determine the month selected
                if location == 'Wodonga Water Treatment Plant ': # ensuring NE Water year starting in MARCH is accounted for (ie, MAR == 0)
                    selectedMonth = values['Month']
                        
                    if selectedMonth == ['January']:
                        month = 10    
                    elif selectedMonth == ['February']:
                        month = 11
                    elif selectedMonth == ['March']:
                        month = 0
                    elif selectedMonth == ['April']:
                        month = 1
                    elif selectedMonth == ['May']:
                        month = 2
                    elif selectedMonth == ['June']:
                        month = 3
                    elif selectedMonth == ['July']:
                        month = 4
                    elif selectedMonth == ['August']:
                        month = 5
                    elif selectedMonth == ['September']:
                        month = 6
                    elif selectedMonth == ['October']:
                        month = 7
                    elif selectedMonth == ['November']:
                        month = 8
                    elif selectedMonth == ['December']:
                        month = 9
                ## TRADITIONAL MONTH ORDERING (ie, JAN 0, FEB = 2 etc)
                elif location == 'External': #ie, ensuring that JAN == 1 - NOT INLCUDED FOR NOW, PLACEHOLDER FOR NEW DATA #BROKEN - FIX LATER
                    if selectedMonth == ['January']:
                        month = 0    
                    elif selectedMonth == ['February']:
                        month = 1
                    elif selectedMonth == ['March']:
                        month = 2
                    elif selectedMonth == ['April']:
                        month = 3
                    elif selectedMonth == ['May']:
                        month = 4
                    elif selectedMonth == ['June']:
                        month = 5
                    elif selectedMonth == ['July']:
                        month = 6
                    elif selectedMonth == ['August']:
                        month = 7
                    elif selectedMonth == ['September']:
                        month = 8
                    elif selectedMonth == ['October']:
                        month = 9
                    elif selectedMonth == ['November']:
                        month = 10
                    elif selectedMonth == ['December']:
                        month = 11

            #do yearly logic
            if values['Year']:  #determine the year
                selectedYear = values['Year'] 
                #do year logic
                if selectedYear == ['2019']:
                    year = 2019
                elif selectedYear == ['2020']:
                    year = 2020




        ### PLOTTING LOGIC GOES HERE
        # print('You are plotting ' + str(interval) + ' data from ' + NE_WATER_MONTHS[month] + ' ' +  str(year) + ' for the ' + str(location) + 'in a plot type of ' + str(plottype)) # FOR TESTING

                ## 2019 DAILY ##
        if interval == 'Daily' and year == 2019: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2019 DAILY MEAN CONSUMPTION'
            Plotter(DAILY_MEAN_2019[month], TITLE = plotTitle , PLOTTYPE = plottype) #daily average
        
                ## 2020 DAILY ##
        elif interval == 'Daily' and year == 2020: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2020 DAILY MEAN CONSUMPTION'
            Plotter(DAILY_MEAN_2020[month], TITLE = plotTitle , PLOTTYPE = plottype) #daily average
            
                ## 2019 WEEKLY ##
        elif interval == 'Weekly' and year == 2019: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2019 WEEKLY MEDIAN CONSUMPTION'
            Plotter(WEEKLY_MEDIAN_2019[month], TITLE = plotTitle , PLOTTYPE = plottype) #Weekly average

                ## 2020 WEEKLY ##    
        elif interval == 'Weekly' and year == 2020: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2020 WEEKLY MEDIAN CONSUMPTION'
            Plotter(WEEKLY_MEDIAN_2020[month], TITLE = plotTitle , PLOTTYPE = plottype) #Weekly average
        else: #error
            print('ERROR MESSAGE')


        

    window.close()

    return #nothing   

def main():
    """ Main fcn"""
    plt.close('all')
    
    ## VARS ##
    
    NE_WATER_MONTHS = {10: 'JAN', 11: 'FEB', 0: 'MAR', 1: 'APR', 2: 'MAY', 3: 'JUN', 4: 'JUL', 5: 'AUG', 6: 'SEP', 7: 'OCT', 8: 'NOV', 9: 'DEC'} 
        #NORTH EAST WATER supplied data starts at MAR, THUS MAR = 0, APR = 1 etc
    
    
    Interval_data_2019_file_name = 'Large Market Interval Data - March 01 2018- Feb 29 2019.xls' #2018/19 data
    Interval_data_2020_file_name = 'Large Market Interval Data - March 01 2019 -March 01 2020.xls' #2019/20 data
    
        ## READING XLS, change to pick which year
    
       
    ## STEP 2 - CALCULATE DAILY AVERAGE PER MONTH ##
    FullIntervalData_2019 = xlsxReader(Interval_data_2019_file_name) #split into months, access via indexing 
    FullIntervalData_2020 = xlsxReader(Interval_data_2020_file_name) #split into months, access via indexing 
    
    DAILY_MEAN_2019 = DailyAverage(FullIntervalData_2019)
    DAILY_MEAN_2020 = DailyAverage(FullIntervalData_2020)
   
    #clear variables to avoid some error. Yes it isnt good practice, 
    FullIntervalData_2019 = None
    FullIntervalData_2020 = None


    ## STEP 3 - CALCULATE WEEKLY AVERAGE PER MONTH ##
    FullIntervalData_2019 = xlsxReader(Interval_data_2019_file_name) #split into months, access via indexing 
    FullIntervalData_2020 = xlsxReader(Interval_data_2020_file_name) #split into months, access via indexing 

    WEEKLY_MEDIAN_2019 = WeeklyAverage(FullIntervalData_2019)
    WEEKLY_MEDIAN_2020 = WeeklyAverage(FullIntervalData_2020) #inconsistent error, not sure why
    
    
    
    ### STEP 4 - PLOTTING GRAPHS ###
    GUI(DAILY_MEAN_2019, DAILY_MEAN_2020, WEEKLY_MEDIAN_2019, WEEKLY_MEDIAN_2020)
    ## STEP 4A - DAILY AVERAGING PLOTS ##
    

    

    return #nothing



### MAIN ###

main()



print('\nCODE \n C\n  O\n   M\n    P\n     L\n      E\n       T\n        E\n         D\n')



### THIS SCRIPT WILL MANIPULATE THE DATA, returning graphable data in the following formats
#
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
# https://pandas.pydata.org/pandas-docs/stable/reference/resampling.html
# https://stackoverflow.com/questions/36681945/group-dataframe-in-5-minute-intervals
# https://stackoverflow.com/questions/17001389/pandas-resample-documentation/17001474#17001474
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
# https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html#visualization-scatter-matrix

# https://gist.github.com/phobson/8d853ddf23d1d692fe4d#file-sac-regression-ipynb - I THINK THIS IS VERY USEFUL 
# https://plotly.com/python/cufflinks/ - makes plotting nice and pretty
    # https://github.com/santosjorge/cufflinks



## OUTPUTS ##
#Average Monthly Hourly Usage


## IDEAS ##
# overlaw solar generation for each individual load to determine best time to turn things on 
# as per drawn image in teams 

## TO DO ##
# make the plotter nicer, currently its a bit hacked together



### V0.1.0

### libraries

import pandas as pd
import datetime as dt
import cufflinks as cf
import matplotlib.pyplot as plt


from pandas.plotting import scatter_matrix

### FUNCTIONS ###


def xlsxReader(input): 
    """reads a given file and returns a list of DF's split into months
    Access said df as via indexing
    ie, JAN = 0
        FEB = 1
        etc
    """
    ### STEP 1 -  read the data without index files
    # data = pd.read_excel(input, parse_dates = True, index_col = 0) #parsed dates and includes an index 
    data = pd.read_excel(input, parse_dates = True, index_col = None) #reads entire df and parses dates without creating an index
    
    months = [g for n, g in data.groupby(pd.Grouper(key='Interval End',freq='M'))] #finally splits it into months,  - is a list, so just access each list as an index (ie, JAN = 0, FEB = 1)
        # FROM https://stackoverflow.com/questions/41625077/python-pandas-split-a-timeserie-per-month-or-week
        # Answer by Toto_Tico
    return months

def MonthToDay(df):
    """Takes 30 minute interval data over the month, and returns an average for a specific day. Returned data is a list of DFs. 
    """
    sampled = [] #empty array
    for x in range (0, 12): # sets each DF to have the correct index
        df[x] = df[x].set_index(['Interval End']) #set the index, as previous DF did not have have an index
        df[x].index = pd.to_datetime(df[x].index, unit='s') # some magic to make it not error out - 
        sampled.append(df[x].groupby([df[x].index.hour, df[x].index.minute]).mean()) #sum each days demand, returns the mean of the hours over the month 
            #REFERENCE FOR THIS https://stackoverflow.com/questions/30579950/grouping-by-30-minutes-space-in-pandas
        
    return sampled

def MonthSUM(df):
    """
    Takes 30 minute interval data over the month, and returns a sum for a each day
    """
    sampled = [] #empty array
    for x in range (0, 12): # sets each DF to have the correct index
        df[x] = df[x].set_index(['Interval End']) #set the index, as previous DF did not have have an index
        df[x].index = pd.to_datetime(df[x].index, unit='s') # some magic to make it not error out - 
        sampled.append(df[x].groupby([df[x].index.hour, df[x].index.minute]).sum()) #sum each days demand 
            #REFERENCE FOR THIS https://stackoverflow.com/questions/30579950/grouping-by-30-minutes-space-in-pandas
    
    return sampled

def MonthToDaySum(df): #fix it up a bit, make it nicer, as it doesnt really work. DISREGARD
    """
    Sums up the entire DF for the month, returns a total energy consumption for each day of the month, as a % of the highest load in each site
    """
    sampled = [] #empty array
    for x in range (0, 12): # sets each DF to have the correct index
        SUMMED = df[x].resample("1D").sum() #sum each days demand 
        SUMMED = df[x].apply(lambda x: x.div(x.max())) #magic lambda function from Sean, divdes X by the max of X, making it into percentages
        sampled.append(SUMMED) #append to all 
            
    return sampled

def Plotter(df, Title = 'DAILY MEAN', XTITLE = 'Time', YTITLE = 'kWh', KIND = 'Subplot'): #this is where things are plotted, will require _some_ manual manipulation until I make it nicer
    """ Plots the given dataframe using cufflinks
    Will require manual manipulation
    """
    ## this is not very well optimised. Will fix/change it later
    rows = 17
    columns = 2
 
    #individual plot
    # fig = df.iplot(asFigure=True, kind = 'box')
    #big boii subplots (ie, 34 graphs)
    if KIND == 'Subplot':
        fig = df.iplot(asFigure=True, subplots=True, shape=(rows, columns), shared_xaxes=True, fill=True, xTitle = XTITLE, yTitle = YTITLE, title = Title) #17 2 is best for portrait monitors, 4 9 is best for landscape monitors
    #nice looking individual plot
    elif KIND == False:
        # fig = df.iplot(asFigure=True, subplots=True, shared_xaxes=True, fill=True, xTitle = XTITLE, yTitle = YTITLE, title = Title) #indivual 
        fig = df.iplot(asFigure=True, xTitle=XTITLE, yTitle=YTITLE, title=Title)
    elif KIND == 'Bar':
        fig = df.iplot(asFigure=True, xTitle=XTITLE, yTitle=YTITLE, title=Title, kind = 'bar')
    


    else:
        print('Incorrect Plot Type')


    fig.show()

    return #nothing

    

def main():
    """ Main fcn"""
    plt.close('all')
    ### STEP 1 - read all xlsx and save as monthly df
        ## VARS
    name19 = 'Large Market Interval Data - March 01 2018- Feb 29 2019.xls' #2018/19 data
    # name20 = 'Large Market Interval Data - March 01 2019 -March 01 2020.xls' #2019/20 data
    
        ## READING XLS
    NEW_2019 = xlsxReader(name19) #split into months, access via indexing 

    ### STEP 2 - Playing with the data

    
    ## DAILY AVERAGE PER MONTH
    NEW_2019_DAILY_MEAN = MonthToDay(NEW_2019)

    ## MONTHLY CONSUMPTION
    # NEW_2019_MONTHLY_CONSUMPTION = MonthToDaySum(NEW_2019) ## DISREGARD, CURRENTLY BROKEN
    
    ## MONTH TO DAILY SUM
    # NEW_MONTHLY_DAILY_SUM = MonthSUM(NEW_2019)
    
    
    ### PLOTTING NICE GRAPHS ###
    
    Plotter(NEW_2019_DAILY_MEAN[0], 'JANUARY DAILY MEAN', KIND = 'Subplot') #change kind to determine what graph is used. 
    # Plotter(NEW_2019_MONTHLY_CONSUMPTION[0], 'JANUARY SUM', KIND = 'Box') ## DISREGARD, CURRENTLY BROKEN
    # Plotter(NEW_MONTHLY_DAILY_SUM[0], 'JANUARY DAILY SUM', KIND = 'Bar')



    return #nothing








### MAIN ###

main()



print('CODE \n C\n  O\n   M\n    P\n     L\n      E\n       T\n        E\n         D\n')




### NOTES ###

# def xlsxReader(input): 
#     """reads a given file and returns a df"""
#     ## read the data 
#     data = pd.read_excel(input, parse_dates = True, index_col = 0) #parsed dates 
#     data2 = data.iloc[:,0:2]
#     # reduced = data[data['VBBB00026601 - Mill Street WODONGA - kWh Consumption']>0.5] # ie. cumulative 30 minute intervals per day that the plant is running



#     # daily = reduced.resample('1D').count() #split the new DF into daily mean 
#     sean = data2.resample("1D").sum() #sum each days demand 


#     sean2 = sean.apply(lambda x: x.div(x.max()))

#     sean2.plot(title = 'MAX Daily as %')
#     plt.show()

#     # daily.plot(title = 'Daily Mean' ) #create the 


#     # data.plot(x = 'Interval End', y = 'VBBB00026601 - Mill Street WODONGA - kWh Consumption', title = 'Dave and Sean' )
#     # fig.savefig("test.png")

#     # plt.show()

#     # daily.to_excel('Daily Mean.xlsx')
#     return #nothing


    ## SEAN STUFF ##
    # sean = data.resample("1D").sum() #sum each days demand 
    # sean2 = sean.apply(lambda x: x.div(x.max())) #lambda function, can be applied to anything I want
    # sean2.plot(title = 'MAX Daily as %')
    # plt.show()

#         ### SOMETHING 
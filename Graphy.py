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



## OUTPUTS ##
#Average Monthly Hourly Usage



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
    """Takes 30 minute interval data over the month, and returns an average for a specific day
    """
    sampled = []
    for x in range (0, 12): # sets each DF to have the correct index
        df[x] = df[x].set_index(['Interval End']) #set the index, as previous DF did not have have an index
        df[x].index = pd.to_datetime(df[x].index, unit='s') # some magic to make it not error out - 
        sampled.append(df[x].groupby([df[x].index.hour, df[x].index.minute]).mean()) #sum each days demand 
            #REFERENCE FOR THIS https://stackoverflow.com/questions/30579950/grouping-by-30-minutes-space-in-pandas
        
        
        ### PROBLEM IS HERE ### NEED TO CONVERT IT TO AVERAGE HOURLY DATA FOR THE ENTIRE MONTH

    ### TESTING ###


    return sampled

def Plotter(df, Title = 'DAILY AVERAGE'):
    """ Plots the given dataframe
    Will require manual manipulation
    """
    
 
    # fig = df.iplot(asFigure=True, kind = 'box')
    fig = df.iplot(asFigure=True, subplots=True, shape=(17,2), shared_xaxes=True, fill=True)
    fig.show()

    return #nothing

    

def main():
    """ Main fcn"""
    plt.close('all')
    ### STEP 1 - read all xlsx and save as monthly df
    name19 = 'Large Market Interval Data - March 01 2018- Feb 29 2019.xls' #2018/19 data
    # name20 = 'Large Market Interval Data - March 01 2019 -March 01 2020.xls' #2019/20 data
    
    NEW_2019 = xlsxReader(name19) #split into months, access via indexing 

    ### STEP 2 - Resample down to 30 hourly data

    NEW_2019_DAILY_MEAN = MonthToDay(NEW_2019)
    # Plotter(NEW_2019_DAILY_MEAN[0].iloc[:,0], 'Test')
    Plotter(NEW_2019_DAILY_MEAN[0],  'Test')
  




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
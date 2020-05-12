#a collection of functions to assist with calculating load during solar hours



import pandas as pd


def DaySummation(monthly_data):
    """
    sums all the data in monthly invertal data, and returns total load for that average day 
    """
    # will have to organise how the data is presented later
    # Totalsummation = []
    # NumberofDataFrames = len(monthly_data)
    # for x in range(0, NumberofDataFrames): # iterate through the list of dataframes
    #     Totalsummation.append(monthly_data[x].sum(axis = 0))   #sum the entire day and append to a dataframe for each month  - NOT SURE THIS IS CORRECT
    Totalsummation = monthly_data.sum(axis = 0)  #sum the entire day and append to a dataframe for each month  - NOT SURE THIS IS CORRECT
    return Totalsummation 

def SolarSlicer(monthly_data, startpost = 18, finishpost = 34):
    """Slices the daily interval data between the startpost and finish post
    only works with daily data (ie, 48xY dataframe)
    """
    # Sliced = []
    # NumberofDataFrames = len(monthly_data)
    # for x in range(0, NumberofDataFrames): # iterate through the list of dataframes
        # Sliced.append(monthly_data[x].iloc[startpost:finishpost, :]) #for slicing, returns every column and and every row between startpost and finishpost. will need to add in a dict to ensure timings 

    Sliced = monthly_data.iloc[startpost:finishpost, :] #for slicing, returns every column and and every row between startpost and finishpost. will need to add in a dict to ensure timings 

    return Sliced
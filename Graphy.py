### THIS SCRIPT WILL MANIPULATE THE DATA, returning graphable data in the following formats
#
#
#
#
#


### V0.1.0

### libraries

import pandas as pd
import datetime as dt


### FUNCTIONS ###

def xlsxReader(input): 
    """reads a given file and returns a df"""
    ## names 
    output = pd.read_excel(input, index_col = None) #no index for later splitting 
    output.set_index('Interval End', drop = False, inplace = True) #set index, and keeps OG date 


    return output

def monthSplitter(df, year = 2019): 
    """ splits the given DF into months, saves each month as a new sheet"""
    
    months_19 = ['JAN_19', 'FEB_19', 'MAR_19', 'APR_19', 'MAY_19', 'JUN_19', 'JUL_19', 'AUG_19', 'SEP_19', 'OCT_19', 'NOV_19', 'DEC_19'] #names of the month (2019 flavour)
    months_20 = ['JAN_20', 'FEB_20', 'MAR_20', 'APR_20', 'MAY_20', 'JUN_20', 'JUL_20', 'AUG_20', 'SEP_20', 'OCT_20', 'NOV_20', 'DEC_20'] #names of the month (2019 flavour)

    df['Interval End'] = pd.to_datetime(df['Interval End']) #magic happens here, ripped straight from SO - https://stackoverflow.com/questions/55974955/splitting-in-pandas-a-timestamp-date/55975035
    
    if year == 2019: 
        for number in range(0, 12): #iterate from JAN (1) to DEC (12)
            months_19[number] = df[df['Interval End'].dt.month == (number + 1)] #adding +1 to number as months dont start

    elif year == 2020: 
        for number in range(0, 12): #iterate from JAN (1) to DEC (12)
            months_20[number] = df[df['Interval End'].dt.month == (number + 1)] #adding +1 to number as months dont start

    ## save DFS as sheets into a xlsx spreadhsheet







    return #nothing


def main():
    """ Main fcn"""

    ### STEP 1 - read all xlsx and save as df
    name19 = 'Large Market Interval Data - March 01 2018- Feb 29 2019.xls' #2018/19 data
    name20 = 'Large Market Interval Data - March 01 2019 -March 01 2020.xls' #2019/20 data
    
    DATA19 = xlsxReader(name19) 
    DATA20 = xlsxReader(name20)

    ### STEP 2 - split each df into monthly sheets
    monthSplitter(DATA19, 2019)
    monthSplitter(DATA20, 2020)

    ### STEP 3 - Average half hourly usage by month

    ### STEP 4 - 




    return #nothing








### MAIN ###

main()



print('CODE \n C\n  O\n   M\n    P\n     L\n      E\n       T\n        E\n         D\n')
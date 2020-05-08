import datetime as dt 
import pandas as pd
import csv 

## quick function to generate dates between two posts

#vars

def dateGEN(start_year = 2019, Interval = 30): 
    """ A Function that creates an empty dataframe to align NE WATER with a JAN to DEC year
    Ie, 1JANYY 00:30 to 31DECYY 00:00 with only the columns (ie, no data)
    """
    ## VARS/HOUSEKEEPING ##
    start_date_time = str(start_year) + '-01-01 00:00:00' #inital staring date, shouldnt have to change this 
    end_date_time = str(start_year) + '-12-31 00:00:00' #ending date, shouldnt have to change this eithe r
    frequency = str(Interval) + 'T' #interval, should stay with 30 minutes. 
    start_time = '00:00' #not entirely sure where this comes from 
    finish_time = '23:30' #or what this does 
    column_name = 'Interval End' #to ensure consistency across multiple dataframe 

    ## GENERATING A LIST OF THE TIME INTERVALS 
    DateList = (pd.DataFrame(columns=['NULL'], #generate the data
                    index=pd.date_range(start_date_time, end_date_time,
                                        freq=frequency))
        .between_time(start_time, finish_time)
        .index.strftime('%Y-%m-%d %H:%M')
        )

    ## CONVERT TO DATAFRAME 
    DateDF = pd.DataFrame(DateList)

    ## INSERT PROPER NAME AT THE TOP 
    DateDF.rename(columns = {0: column_name}, inplace = True) #insert the proper interval end tag as a header
    
    ## CONVERT INTERVAL END TO DATETIME 
    DateDF[column_name] = pd.to_datetime(DateDF[column_name])
    
    ## SPLIT INTO MONTHS 
    # months = [g for n, g in DateDF.groupby(pd.Grouper(key='Interval End',freq='M'))] #splits it into months
        # is a list, so just access each list as an index (ie, JAN = 0, FEB = 1)
        # https://stackoverflow.com/a/49491178/13181119
    
    return DateDF

Empty = dateGEN(2018, 60)
Empty.to_csv('2018_EMPTY.csv')
# print(Empty)
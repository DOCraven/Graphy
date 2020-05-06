import pandas as pd
# import datetime as dt
import cufflinks as cf
# import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
# from calendar import day_name
import PySimpleGUI as sg




def Plotter(df, TITLE = 'DAILY MEAN', X_LABEL = 'Time', Y_LABEL = 'kWh', PLOTTYPE = 'Subplot'): #this is where things are plotted, will require _some_ manual manipulation until I make it nicer
    """ 
    Plots the given dataframe using cufflinks
    """
    ## determing the rows/columns for subplots, change this to output for your screen
    # plotting types
    #nice looking individual plot
    if PLOTTYPE == 'Individual':
        fig = df.iplot(asFigure=True, xTitle=X_LABEL, yTitle=Y_LABEL, title=TITLE)
    elif PLOTTYPE == 'Bar':
        fig = df.iplot(asFigure=True, xTitle=X_LABEL, yTitle=Y_LABEL, title=TITLE, kind = 'bar')
    elif PLOTTYPE == 'Histogram':
        fig = df.iplot(asFigure=True, xTitle=X_LABEL, yTitle=Y_LABEL, title=TITLE, kind = 'histogram')
    elif PLOTTYPE == 'Box':
        fig = df.iplot(asFigure=True, xTitle=X_LABEL, yTitle=Y_LABEL, title=TITLE, kind = 'box')
    else:
        print('Incorrect Plot Type')

    fig.show() #show the figure in the default web browser

    return #nothing

def GUI(DAILY_MEAN_2018 = None, DAILY_MEAN_2019 = None, DAILY_MEAN_2020 = None, WEEKLY_MEDIAN_2018 = None, WEEKLY_MEDIAN_2019 = None, WEEKLY_MEDIAN_2020 = None): 
    """ 
    A simple GUI to make plotting easier and interactive 
    """
    ## VARS
    Months = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
    Year = ('2018', '2019', '2020')
    Interval = ('Daily', 'Weekly')
    Plot = ('Individual', 'Bar',  'Histogram', 'Box')
    
    NE_WATER_MONTHS = {0: 'JAN', 1: 'FEB', 2: 'MAR', 3: 'APR', 4: 'MAY', 5: 'JUN', 6: 'JUL', 7: 'AUG', 8: 'SEP', 9: 'OCT', 10: 'NOV', 11: 'DEC'} #dict for accessing months
    plottype = interval = month = year = None #so scope doesnt screw me. Could use a global var, but this is less typing
    
    #determining the layout
    layout = [  [sg.Text('Plotting Options')],
            [sg.Text('Pick a year', size = (12, None)), sg.Listbox(Year, size=(20, len(Year)), key='Year')],
            [sg.Text('Pick a Month', size = (12, None)), sg.Listbox(Months, size=(20, len(Months)), key='Month')],
            [sg.Text('Pick a Data \nOutput Format', size = (12, None)), sg.Listbox(Interval, size=(20, len(Interval)), key='Interval')],
            [sg.Text('Pick a Plot Type', size = (12, None)), sg.Listbox(Plot, size=(20, len(Plot)), key='Plot Type')],
            [sg.Button('Plot'), sg.Button('Exit')]  ] #sg.Button('Save .CSV'), for future addon

    window = sg.Window('NE WATER GRAPHY', layout) #open the window

    while True: # so the window is peristent
        event, values = window.read() #keep waiting for a user input
        if event is None:
            break
        if event == 'Plot': #ie, plot button is pushed, so plot the selected time/date/average
            if values['Interval']: #determine the interval 
                selectedInterval = values['Interval']
                #do location logic
                if selectedInterval == ['Daily']: 
                    interval = 'Daily'
                elif selectedInterval == ['Weekly']:
                    interval = 'Weekly'
            else: 
                print('please select a interval type')
            
            if values['Plot Type']: #determine the Plot Type 
                selectedPlot = values['Plot Type']
                #do location logic
                if selectedPlot == ['Subplot']: 
                    plottype = 'Subplot'
                elif selectedPlot == ['Individual']:
                    plottype = 'Individual'
                elif selectedPlot == ['Bar']:
                    plottype = 'Bar'
                elif selectedPlot == ['Histogram']:
                    plottype = 'Histogram'
                elif selectedPlot == ['Box']:
                    plottype = 'Box'
            else: 
                print('please select a plot type')
                    
            #do month logic
            if values['Month']:    # Determine the month selected
                selectedMonth = values['Month']
                
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
            else: 
                print('please select a month')
            
            #do yearly logic
            if values['Year']:  #determine the year
                selectedYear = values['Year'] 
                #do year logic
                if selectedYear == ['2018']:
                    year = 2018
                elif selectedYear == ['2019']: 
                    year = 2019
                elif selectedYear == ['2020']:
                    year = 2020
            else: 
                print('please select a year')
        
        elif event == 'Exit': #ie, exit button is pushed so quit 
            window.close()

        ### ONLY PLOTTING DATA ###
                ## 2019 DAILY ##
        if interval == 'Daily' and year == 2018: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2018 DAILY MEAN CONSUMPTION'
            Plotter(DAILY_MEAN_2018[month], TITLE = plotTitle , PLOTTYPE = plottype) #daily average
        
                ## 2019 DAILY ##
        elif interval == 'Daily' and year == 2019:
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2019 DAILY MEAN CONSUMPTION'
            Plotter(DAILY_MEAN_2019[month], TITLE = plotTitle , PLOTTYPE = plottype) #daily average 

                ## 2020 DAILY ##
        elif interval == 'Daily' and year == 2020: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2020 DAILY MEAN CONSUMPTION'
            Plotter(DAILY_MEAN_2020[month], TITLE = plotTitle , PLOTTYPE = plottype) #daily average
            
                ## 2018 WEEKLY ##
        elif interval == 'Weekly' and year == 2018: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2018 WEEKLY MEDIAN CONSUMPTION'
            Plotter(WEEKLY_MEDIAN_2018[month], TITLE = plotTitle , PLOTTYPE = plottype) #Weekly average

                ## 2019 WEEKLY ##    
        elif interval == 'Weekly' and year == 2019: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2019 WEEKLY MEDIAN CONSUMPTION'
            Plotter(WEEKLY_MEDIAN_2019[month], TITLE = plotTitle , PLOTTYPE = plottype) #Weekly average

                ## 2020 WEEKLT ##
        elif interval == 'Weekly' and year == 2020: 
            plotTitle = str(NE_WATER_MONTHS[month]) + ' 2020 WEEKLY MEDIAN CONSUMPTION'
            Plotter(WEEKLY_MEDIAN_2020[month], TITLE = plotTitle , PLOTTYPE = plottype) #Weekly average
        else: #error
            print('Please select Interval or Year')
        
            
        
   
    window.close()

    return #nothing   


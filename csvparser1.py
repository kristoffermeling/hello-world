# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 12:14:42 2019
@author: melingk1
"""

# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
#%matplotlib inline
import matplotlib.pyplot as plt
#import matplotlib.dates as md
import datetime as dt
import time
from datetime import datetime
from os import scandir
import os
from pathlib import Path
import math


#function to check if csv date is in 24 hr and european style format
def formatting_check24hr_nor(input):
    try:
        time.strptime(input,'%d.%m.%Y %H:%M:%S')
    except:
        return False
    else:
        return True
            
#function to check if csv date is in murica format
def formatting_check12hr_american(input):
    try:
        time.strptime(input,'%m/%d/%Y %I:%M:%S %p')
    except:
        return False
    else:
        return True









# =============================================================================
# def convert_date(timestamp):
#     d = datetime.utcfromtimestamp(timestamp)
#     formated_date = d.strftime('%d %b %Y')
#     return formated_date
# =============================================================================
#import the contents of a folder
# =============================================================================
# 
# def get_files():
#     dir_entries = scandir('C:/Users/Kristoffer/Desktop/python/testing')
#     for entry in dir_entries:
#         if entry.is_file():
#             info = entry.stat()
#             print(f'{entry.name}\t Last Modified: {convert_date(info.st_mtime)}')
# 
# =============================================================================

#def parse_and_print(f_name):

f_name='dPinletAandB3month.csv'
index = pd.read_csv(f_name,nrows = 0, delimiter =" ")
df = pd.read_csv(f_name,skiprows=1 ,delimiter="\t")

col=df.columns


if col.size>=3:
    varA=df.loc[:,col[1]]
    date=df.loc[:,col[0]]
    varB=df.loc[:,col[2]]
    
elif col.size >= 2:    
    varA=df.loc[:,col[1]]
    date=df.loc[:,col[0]]
    
elif col.size>=1:
    date=df.loc[:,col[0]]
   
#the available date formats
formattAMPM = '%m/%d/%Y %I:%M:%S %p'
formatt24hr = '%d.%m.%Y %H:%M:%S'

#check what format the data is
if formatting_check24hr_nor(date[1]):
    dates=[datetime.strptime(date,formatt24hr) for date in date]
elif formatting_check12hr_american(date[1]):
    dates=[datetime.strptime(date,formattAMPM) for date in date]
#if csv use comma as decimal delimiter, then this must be changed to "."    
if isinstance(varA[0],str):
    varA[:] = varA.replace(',','.', regex=True)
    varA[:]=varA.astype(float)
if isinstance(varB[0],str):
    varB[:] = varB.replace(',','.', regex=True)
    varB[:]=varB.astype(float)

varA_average = varA.mean() 
varB_average = varB.mean() 
avg_diff = abs(varA_average - varB_average)

#decide if both column A and B contain valid values that can be plotted
if 'varB'in globals() and not math.isnan(varA[0]) and not math.isnan(varB[0]):
    if avg_diff > 200:
        fig, ax1 = plt.subplots()
        ax1.set_ylabel(col[1])
        ax1.plot(dates,varA)
        
        ax2 = ax1.twinx()
        ax2.set_ylabel(col[2])
        ax2.plot(dates,varB)
        #fig.thight_layout()
        plt.xlabel('Dates')
        plt.xticks(rotation=45)
        #plt.show()
        
    else:
        plt.ylabel(col[1]+'   '+ col[2])
        plt.plot(dates,varA)
        plt.plot(dates,varB)
        plt.xlabel('Dates')
        plt.xticks(rotation=45)
    
    


    
elif not math.isnan(varA[0]):
    plt.ylabel(col[1])
    plt.plot(dates, varA)
    plt.xlabel('Dates')
    plt.xticks(rotation=45)
elif not math.isnan(varB[0]):
    plt.ylabel(col[2])    
    plt.plot(dates, varB)
    plt.xlabel('Dates')
    plt.xticks(rotation=45)
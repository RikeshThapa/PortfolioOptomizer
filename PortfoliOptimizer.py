'''
The purpose of this function is to simulate and assess the perormance of a 4 stock portfolio
Inputs: 
	- Start Date
	- End Date
	- Symbols for the equities (eg. GOOG, AAPL, GLD, XOM)
	- Allocations to the equities at the beginning of the simulation (e.g. 0.2, 0.3, 0.4, 0.1)
Outputs:
	- Standard deviation of daily returns of the total portfolio 
	- Average daily return of the total portfolio
	- Sharpe ratio (252 trading days in a year at risk free rate = 0) of the total portfolio
	- Cumulative return of the total portfolio
	
Example execution:
vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, ['GOOG', 'AAPL', 'GLD', 'XOM'), [0.2, 0.3. 0.4, 0.1])

'''

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd


ls_symbols = ["GOOG", "APPL", "GLD", "XOM"]  # Equities being passed as paramenters
dt_start = dt.datetime(2006, 1, 1)			 # Start date specification
dt_end = dt.datetime(2010, 12, 31)			 # End date specification
dt_timeofday = dt.timedelta(hours=16)		#This gives us the data that was available at the close of the day
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday) #list of timestamps that represent NYSE closing times between teh start and end dates

c_dataobj = da.DataAccess('Yahoo')			#Create object that reads from Yahoo datasource
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']		#The data types that i would like to read
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)			# Data frome with all the different data
d_data = dict(zip(ls_keys, ldf_data))			# Convert dataframe to dictionary so it can be accessed easily

na_price = d_data["close"].values  #List of closing prices put into 2D numpy array
plt.clf()						 # Clearsprevious graphs that may have been drawn on matplotlib
plt.plot(ldt_timestamps, na_price) #Plot the data in na_price
plt.legend(ls_symbols)				#This line and below are just legends and colors
plt.ylabel('Adjusted Close')
plt.xlabel('Date')
plt.savefig('adjustedclose.pdf', format='pdf')

na_normalized_price = na_price[0, :]/na_price[0, :] #Normalize the data with respect to teh first day's price
for n in na_normalized_price:
	print n
#daily returns for day t:
#(ret(t) = price(t-1))-1

na_rets = na_normalized_price.copy()
returns = tsu.returnize0(na_rets)
print returns


import pandas as pd 
import matplotlib.pyplot as plt
import datetime 
from pylab import rcParams

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

n = 30 #the number of days of data you wish to see

daily_us = pd.read_json('https://covidtracking.com/api/v1/us/daily.json')

daily_us = daily_us.loc[:, ['date', 'positive', 'negative', 'death', 'totalTestResults']]

daily_us = daily_us.sort_values('date', ascending = False)
daily_us['date'] = daily_us['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
daily_us = daily_us.set_index('date')
daily_us = daily_us.dropna()
print ('\n', daily_us.head(n))

daily_us['totalTestResults'] = daily_us['totalTestResults'].div(1000)

rcParams['figure.figsize'] = 15, 10
plt.plot(daily_us['totalTestResults'])
plt.title(f'Total Test Results for USA in the Thousands')
plt.xlabel('Date')
plt.ylabel('Total Test Results')
plt.show()
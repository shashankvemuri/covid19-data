import pandas as pd 
import matplotlib.pyplot as plt
import datetime 
from pylab import rcParams

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

n = 30 #the number of days of data you wish to see

daily_us = pd.read_json('https://covidtracking.com/api/v1/us/daily.json')

daily_us = daily_us.loc[:, ['date', 'positive', 'negative', 'death', 'totalTestResults']]

daily_us['testPositivityRate'] = round(daily_us['positive'] * 100 / daily_us['totalTestResults'], 2)
daily_us['difference'] = round(daily_us['testPositivityRate'].pct_change(), 2)

daily_us = daily_us.sort_values('date', ascending = False)
daily_us['date'] = daily_us['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
daily_us = daily_us.set_index('date')
daily_us = daily_us.dropna()
print ('\n', daily_us.head(n))

rcParams['figure.figsize'] = 15, 10
plt.plot(daily_us['testPositivityRate'])
plt.title(f'Test Positivity Rate for USA')
plt.xlabel('Date')
plt.ylabel('Test Positivity Rate in %')
plt.show()
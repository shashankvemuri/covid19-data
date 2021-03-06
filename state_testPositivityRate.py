import pandas as pd 
import matplotlib.pyplot as plt
import datetime 
from pylab import rcParams

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

daily_state = pd.read_json('https://covidtracking.com/api/v1/states/daily.json')

daily_state = daily_state.loc[:, ['date', 'state', 'positive', 'negative', 'death', 'totalTestResults']]

daily_state['testPositivityRate'] = round(daily_state['positive'] * 100 / daily_state['totalTestResults'], 2)
daily_state['difference'] = round(daily_state['testPositivityRate'].pct_change(), 2)

val = str(input('Enter a state: '))
val = val.upper()
val = val.strip()
my_list = ['{}'.format(val)]


if my_list[0] in daily_state['state'].tolist():
    states = pd.read_csv('state_codes.csv', index_col=0)
    states = states.drop(columns = ['Abbrev'])

    daily_state = daily_state.set_index('state')
    daily_state = daily_state[daily_state.index.isin(my_list)]
    daily_state = daily_state.reset_index()
    daily_state = daily_state.drop(columns = ['state'])
    
    daily_state = daily_state.sort_values('date', ascending = False)
    daily_state['date'] = daily_state['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
    daily_state = daily_state.set_index('date')
    daily_state = daily_state.dropna()
    daily_state.columns = ['pos', 'neg', 'death', 'totalTests', 'testPositivityRate', 'diff']
    print ('\n', daily_state.head())
    
    plt.gcf()
    rcParams['figure.figsize'] = 14, 7
    plt.plot(daily_state['testPositivityRate'])
    state_name = states[states['Code']==f'{val}'].index.values
    plt.title(f'Test Positivity Rate for {state_name[0]}')
    plt.xlabel('Date')
    plt.ylabel('Test Positivity Rate in %')
    plt.show()

elif my_list[0].lower() == 'help'.lower():
    print ('\nHere is a DataFrame of states and their respective abbreviations:')
    states = pd.read_csv('state_codes.csv', index_col=0)
    states = states.drop(columns = ['Abbrev'])
    print (states)
    
else: 
    print ('\nEnter a valid state abbreviation! Here is a DataFrame of states and their respective abbreviations:')
    states = pd.read_csv('state_codes.csv', index_col=0)
    states = states.drop(columns = ['Abbrev'])
    print (states)
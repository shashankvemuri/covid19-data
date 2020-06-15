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

daily_state = daily_state.sort_values('date', ascending = False)
daily_state['date'] = daily_state['date'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
daily_state = daily_state.set_index('date')
daily_state = daily_state.dropna()
daily_state.columns = ['state', 'pos', 'neg', 'death', 'totalTests', 'testPositivityRate', 'diff']

states = daily_state.state.tolist()
df_dict = {state: daily_state.loc[daily_state['state'] == state] for state in states}

A = []
B = []
C = []
D = []
E = []

for state in states:
    testPositivityRate = df_dict[state].testPositivityRate.tolist()
    last_rate = testPositivityRate[0]

    if last_rate < 5:
        A.append(state)

    elif last_rate > 5 and last_rate < 15:
        B.append(state)

    elif last_rate > 15 and last_rate < 25:
        C.append(state)  

    elif last_rate > 25:
        D.append(state)
    
print ('Grade A: ')
if not A:
    print ('There are no states that have a grade of A')
else:
    A = pd.Series(A).drop_duplicates().tolist()
    print('[',end='');print(*A, sep=', ', end='');print(']')

print ('\nGrade B: ')
if not B:
    print ('There are no states that have a grade of B')
else:
    B = pd.Series(B).drop_duplicates().tolist()
    print('[',end='');print(*B, sep=', ', end='');print(']')

print ('\nGrade C: ')
if not C:
    print ('There are no states that have a grade of C')
else:
    C = pd.Series(C).drop_duplicates().tolist()
    print('[',end='');print(*C, sep=', ', end='');print(']')

print ('\nGrade D: ')
if not D:
    print ('There are no states that have a grade of D')
else:
    D = pd.Series(D).drop_duplicates().tolist()
    print('[',end='');print(*D, sep=', ', end='');print(']')
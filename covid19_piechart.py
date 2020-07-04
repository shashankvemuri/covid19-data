import numpy as np
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

import webbrowser
website = 'https://www.worldometers.info/coronavirus/'
webbrowser.open(website)

data = pd.read_clipboard()
print (data)
data.columns = ['Country','TotalCases','NewCases','TotalDeaths','NewDeaths','TotalRecovered','ActiveCases','CriticalCondition','TotCasesPerMillion','DeathsPerMillion','TotalTests','TestsPerMillion']

for x in range(1,len(data.columns)):
    data[data.columns[x]] = data[data.columns[x]].str.replace(',','') 
data = data.fillna(0)

for i in range (1,len(data.columns)):
    data[data.columns[i]] = data[data.columns[i]].astype(float).astype(int)

data['DeathRate'] = data['TotalDeaths']/data['TotalCases']
data.sort_values(by=['DeathRate'], inplace=True, ascending=False)

df=data[['Country','DeathRate']].head(15) #select two columns and top 15 rows
df['DeathRate'] = (df['DeathRate']*100).round(1)

c = df['Country'].values.tolist()
d = df['DeathRate'].values.tolist()

color_series = ['#802200','#B33000','#FF4500','#FAA327','#9ECB3C',
 '#6DBC49','#37B44E','#14ADCF','#209AC9','#1E91CA',
 '#2C6BA0','#2B55A1','#2D3D8E','#44388E','#6A368B',
 '#D02C2A','#D44C2D','#F57A34','#FA8F2F','#D99D21']

rosechart = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
rosechart.set_colors(color_series)

rosechart.add("", [list(z) for z in zip(c, d)],
        radius=["20%", "95%"],  # 20% inside radius，95% ourside radius
        center=["30%", "60%"],   # center of the chart
        rosetype="area")

rosechart.set_global_opts(title_opts=opts.TitleOpts(title='Nightingale Rose Chart',subtitle="Covid-19 Death Rate"),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
rosechart.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,formatter="{b}:{c}%", font_style="italic",font_weight="bold", font_family="Century"),)
rosechart.render_notebook()
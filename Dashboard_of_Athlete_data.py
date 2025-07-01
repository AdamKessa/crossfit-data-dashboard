import numpy as np
import lightningchart as lc
import pandas as pd
from click import style
from lightningchart import Dashboard

#%%
df = pd.read_csv('athletes.csv')

lc.set_license('Licence')
#Pie data

df = df[df['gender'] != '--']

# Calculate the counts of each gender
gender_counts = df['gender'].value_counts()

# Calculate the total count
total_count = gender_counts.sum()

# Prepare the data for the pie chart with percentages
data = []
for gender, count in gender_counts.items():
    percentage = (count / total_count) * 100
    data.append({'name': f'{gender} ({percentage:.2f}%)', 'value': int(count)})

# Create the pie chart
dashboard = lc.Dashboard(columns=2, rows=2, theme=lc.Themes.CyberSpace)

pie_chart = dashboard.PieChart(column_index=0, row_index=0)
pie_chart.set_title("Sex ratio of Athletes")

# Separate the slices with white stroke
pie_chart.set_slice_stroke(color=lc.Color('white'), thickness=1)

pie_chart.add_slices(data)

pie_chart.add_legend(data=pie_chart)

#### Weight Histogram

#creating weight_kg column
df['weight_kg'] = df['weight'] * 0.453592

# Filtering out relevant data (representative of the bulk of crossfit athletes)
df = df[(df['weight_kg'] < 110) & (df['weight_kg'] >= 45)]
#
#Creating CrossFit athlete Age histogram
weight_data = df.dropna(subset=['weight_kg'])['weight_kg']

bin_counts, bin_edges = np.histogram(weight_data, bins= weight_data.nunique())
bin_edges = np.round(bin_edges).astype(int)

#setting up histogram data
histogram_data = [
    {'category': f'{bin_edges[i]}', 'value': int(bin_counts[i])}
    for i in range(len(bin_edges) - 1)
]

#calculating median and quartiles
median = np.median(weight_data)
median = np.round(median).astype(int)
q1, q3 = np.percentile(weight_data, [25, 75])
q1, q3 = np.round(q1).astype(int), np.round(q3).astype(int)

#Initializing chart
chart = dashboard.BarChart(column_index=1, row_index=0)
chart.set_title(title=f'Weight Distribution in Kgs of {len(weight_data)} CrossFit Athletes')

chart.set_data(histogram_data)
chart.set_sorting('disabled')

#Setting up median and quartiles indicators
textbox = chart.add_textbox(position_scale='percentage', text="Median")
textbox.set_position(x=52, y=24.5)

textbox = chart.add_textbox(position_scale='percentage', text="q1")
textbox.set_position(x=36.5, y=21.5)

textbox = chart.add_textbox(position_scale='percentage', text="q3", )
textbox.set_position(x=65, y=22)

#Coloring median and quartiles bars
chart.set_bars_color(lc.Color('lightgreen'))
chart.set_bar_color(str(median), lc.Color('wheat'))
chart.set_bar_color(str(q1), lc.Color('midnightblue'))
chart.set_bar_color(str(q3), lc.Color('orchid'))

# dashboard.open()

########## Age Histogram

# Filtering out relevant data
df = df[ (df['age']<60) ]
#Creating CrossFit athlete Age histogram
age_data = df.dropna(subset=['age'])['age']
bin_counts, bin_edges = np.histogram(age_data, bins= age_data.nunique())
bin_edges = np.round(bin_edges).astype(int)

#setting up histogram data
categories = [
    {'category': f'{bin_edges[i]}', 'value': int(bin_counts[i])}
    for i in range(len(bin_edges) - 1)
]

# calculating median and quartiles
q1, q3 = np.percentile(age_data, [25, 75]).astype(int)
median = np.median(age_data).astype(int)

chart = dashboard.BarChart(column_index=0, row_index=1)
chart.set_title(title=f'Age Distribution of {len(age_data)} CrossFit Athletes')
chart.set_data(categories)
# chart.add_legend().add(chart) Legend doesn't work properly.

#Setting up median and quartiles indicators
textbox = chart.add_textbox(position_scale='percentage', text="Median")
textbox.set_position(x=46.3, y=90)

textbox = chart.add_textbox(position_scale='percentage', text="q1")
textbox.set_position(x=36.5, y=92)

textbox = chart.add_textbox(position_scale='percentage', text="q3", )
textbox.set_position(x=57.9, y=52.7)

chart.set_bars_color(lc.Color('lightgreen'))
chart.set_bar_color(str(median), lc.Color('wheat'))
chart.set_bar_color(str(q1), lc.Color('midnightblue'))
chart.set_bar_color(str(q3), lc.Color('orchid'))

chart.set_sorting('disabled')

# dashboard.open(method="browser")

######Height histogram

df.loc[:, 'height_meters'] = df['height'] * 0.0254
df.loc[:, 'height_meters'] = df['height_meters'].round(2)
#Filtering out relevant data
df = df[(df['height_meters'] < 2) & (df['height_meters'] >= 1.45)]
#Dropping null values and creating Athlete height data and histogram
height_data = df.dropna(subset=['height_meters'])['height_meters']

bin_counts, bin_edges = np.histogram(height_data, bins= height_data.nunique())
bin_edges = np.round(bin_edges, 2)

#setting up histogram data
histogram_data = [
    {'category': f'{bin_edges[i]}', 'value': int(bin_counts[i])}
    for i in range(len(bin_edges) - 1)
]

#calculating median and quartiles
# median = np.median(height_data)
# median = np.round(median, 2)
# q1, q3 = np.percentile(height_data, [25, 75])
# q1, q3 = np.round(q1, 2), np.round(q3, 2)

#Initializing chart
chart = dashboard.BarChart(column_index=1, row_index=1)
chart.set_title(title=f'Height Distribution in Meters of {len(height_data)} CrossFit Athletes')

chart.set_data(histogram_data)
chart.set_sorting('disabled')

#Coloring median and quartiles bars
chart.set_bars_color(lc.Color('midnightblue'))

dashboard.open(method='browser')
import lightningchart as lc
import pandas as pd

#%%
df = pd.read_csv('athletes.csv')

lc.set_license('Licence')
df.head()

stats_and_performance_features = df[
    ['age',
     'height_meters',
     'weight_kg',
     'run400',
     'run5k',
     'snatch',
     'deadlift',
     'backsq',
     'pullups'
    ]
]

#Cleaning the selected features

# Removing the upper outliers
df = df[ (df['run400']<150) ]

# Removing the lower outliers
df = df[ (df['run400']>44) ]

# run5k feature

# Removing the upper outliers
df = df[ (df['run5k']<2101) ]

# Removing the lower outliers
df = df[ (df['run5k']>910) ]

# snatch feature

# Removing the upper outliers
df = df[ (df['snatch']<301) ]

# Removing the lower outliers
df = df[ (df['snatch']>55) ]

# deadlift feature

# Removing the upper outliers
df = df[ (df['deadlift']<630) ]

# Removing the lower outliers
df = df[ (df['deadlift']>160) ]

# backsq feature

# Removing the upper outliers
df = df[ (df['backsq']<540) ]

# Removing the lower outliers
df = df[ (df['backsq']>124) ]

# pullups feature


# Removing the upper outliers
df = df[ (df['pullups']<80) ]

# Removing the lower outliers
df = df[ (df['pullups']>0) ]

# Compute correlation matrix
corr_matrix = stats_and_performance_features.corr()
corr_array = corr_matrix.to_numpy()

# Extract min and max correlation values
min_value = corr_array.min()
max_value = corr_array.max()

# Create LightningChart Heatmap
chart = lc.ChartXY(
    title="Correlation Map of Athlete Performance Features",
    theme=lc.Themes.CyberSpace
)

grid_size_x, grid_size_y = corr_array.shape

heatmap_series = chart.add_heatmap_grid_series(
    columns=grid_size_x,
    rows=grid_size_y,
)

heatmap_series.set_start(x=0, y=0)
heatmap_series.set_end(x=grid_size_x, y=grid_size_y)
heatmap_series.set_step(x=1, y=1)
heatmap_series.set_wireframe_stroke(thickness=1, color=lc.Color('lightgrey'))

# Assign correlation values to heatmap
heatmap_series.invalidate_intensity_values(corr_array.tolist())
heatmap_series.set_intensity_interpolation(False)

# Define color scale
palette_steps = [
    {"value": min_value, "color": lc.Color('blue')},  # Negative correlation
    {"value": 0, "color": lc.Color('white')},  # No correlation
    {"value": 1, "color": lc.Color('red')}  # Strong positive correlation
]

heatmap_series.set_palette_coloring(
    steps=palette_steps,
    look_up_property='value',
    interpolate=True
)

# Customize X and Y Axes
x_axis = chart.get_default_x_axis()
y_axis = chart.get_default_y_axis()

x_axis.set_tick_strategy('Empty')
y_axis.set_tick_strategy('Empty')

# Add feature names as axis labels
feature_names = stats_and_performance_features.columns.tolist()
for i, label in enumerate(feature_names):
    custom_tick_x = x_axis.add_custom_tick().set_tick_label_rotation(90)
    custom_tick_x.set_value(i + 0.5)
    custom_tick_x.set_text(label)

    custom_tick_y = y_axis.add_custom_tick()
    custom_tick_y.set_value(i + 0.5)
    custom_tick_y.set_text(label)

# Add legend
chart.add_legend(data=heatmap_series).set_margin(-20)

# Show chart
chart.open(method="browser")
print(f"Min correlation: {min_value}, Max correlation: {max_value}")


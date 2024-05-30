import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Legend
from bokeh.palettes import Category10
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.models import ColumnDataSource
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.io import show,output_file
from bokeh.transform import cumsum
from math import pi
from bokeh.palettes import Category20c
from bokeh.palettes import Category10
from io import StringIO
from bokeh.transform import dodge
import numpy as np
from bokeh.models import LinearColorMapper
from bokeh.layouts import gridplot


df=pd.read_csv('data1.csv')
df1=df[df['Milieu de résidence']=='National'] 
df1=df1[df1['Sexe']=='Total'] 
df1
df0=df[df['Milieu de résidence']=='National'] 

output_file("x.html")

#Visualisation 1

p1 = figure(title="Total Unemployment by Duration and Year (National)", x_axis_label='Year', y_axis_label='Total')
years = [str(year) for year in range(1999, 2022)]
colors = Category10[len(df1)]
for (duree, color) in zip(df1['Durée de chômage'].unique(), colors):
    subset = df1[df1['Durée de chômage'] == duree]
    source = ColumnDataSource(data={
        'year': [int(year) for year in years],
        'total': subset[years].values.flatten()
    })
    p1.line('year', 'total', source=source, line_width=2, color=color, legend_label=duree)

p1.legend.title = "Durée de chômage"
p1.legend.location = "top_left"
p1.grid.grid_line_alpha = 0.3

#
sexes = ['Masculin', 'Feminin']

df0=df0[df0['Durée de chômage']=='Moins de 12 mois']
df2=df0[df0['Sexe']=='Total'] 
df3=df0[df0['Sexe']=='Feminin'] 
df2
data = {
    'years': years,
    'Masculin': df2[years].values.flatten(),
    'Feminin': df3[years].values.flatten(),
}
source = ColumnDataSource(data=data)

#Visualisation 2
p2 = figure(x_range=years, height=400, width=800, title="Chomage de moins de 12 mois par sexe pour chaque année",
           toolbar_location=None, tools="")

# Add stacked bars
p2.vbar_stack(sexes, x='years', width=0.9, color=['#718dbf', '#e84d60'], source=source, legend_label=sexes)
# Configure the plot
p2.y_range.start = 0
p2.xgrid.grid_line_color = None
p2.axis.minor_tick_line_color = None
p2.outline_line_color = None
p2.xaxis.major_label_orientation = 1.2
p2.legend.title = 'Sexe'
p2.legend.location = "top_left"
p2.legend.orientation = "horizontal"

#
df4=df[df['Milieu de résidence']=='National'] 
df4=df4[df4['Durée de chômage']=='60 mois et plus']
df2=df4[df4['Sexe']=='Masculin '] 
df3=df4[df4['Sexe']=='Feminin'] 
df2
data = {
    'years': years,
    'Masculin': df2[years].values.flatten(),
    'Feminin': df3[years].values.flatten(),
}

source = ColumnDataSource(data=data)
#Visualisation 3
# Define the bar chart
p3 = figure(x_range=years, height=400, width=800, title="Chomage de moins de plus de 60 mois par sexe pour chaque année",
           toolbar_location=None, tools="")

# Add stacked bars
p3.vbar_stack(sexes, x='years', width=0.9, color=['#718dbf', '#e84d60'], source=source, 
             legend_label=sexes)

# Configure the plot
p3.y_range.start = 0
p3.xgrid.grid_line_color = None
p3.axis.minor_tick_line_color = None
p3.outline_line_color = None
p3.xaxis.major_label_orientation = 1.2
p3.legend.title = 'Sexe'
p3.legend.location = "top_left"
p3.legend.orientation = "horizontal"

#
data = {
    "Milieu de résidence": ["Urbain", "Rural"],
    "2020": [15.8, 5.9]
}

df = pd.DataFrame(data)
data = df.set_index("Milieu de résidence")["2020"]
data = data / data.sum() * 100 
data = data.reset_index(name='value').rename(columns={'Milieu de résidence': 'milieu'})
data['angle'] = data['value'] / 100 * 2 * pi
colors = ["#1f77b4", "#ff7f0e"]
data['color'] = colors[:len(data)]
#Visualisation 4
p4 = figure(height=350, title="Taux de chômage en 2020", toolbar_location=None,
           tools="hover", tooltips="@milieu: @value{0.2f}%", x_range=(-0.5, 1.0))

p4.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='milieu', source=data)

p4.axis.axis_label = None
p4.axis.visible = False
p4.grid.grid_line_color = None

#
data = {
    "Diplôme": [
        "enseignement fondamental", 
        "enseignement secondaire", 
        "l'enseignement supérieur", 
        "technicien et de cadre moyen", 
        "qualification professionnelle", 
        "spécialisation professionnelle", 
        "sans diplôme"
    ],
    "1999": [25.4, 32.5, 32.9, 19.8, 34, 39.7, 13.8]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Prepare data for the radial plot
data = df.set_index("Diplôme")["1999"]
data = data / data.sum() * 100  # Convert to percentages
data = data.reset_index(name='value').rename(columns={'Diplôme': 'diplome'})

# Compute the angle for each sector
data['angle'] = data['value'] / 100 * 2 * pi

# Use a color palette
data['color'] = Category20c[len(data)]

#Visualisation 5
p5 = figure(height=350, title="Distribution of Diplômes for 1999 (National)", toolbar_location=None,
           tools="hover", tooltips="@diplome: @value{0.2f}%", x_range=(-0.5, 1.0))

p5.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='diplome', source=data)

p5.axis.axis_label = None
p5.axis.visible = False
p5.grid.grid_line_color = None

#
data = {
    "Year": [2010, 2020],
    "Value": [9.0, 9.2]
}

# Create a DataFrame
df = pd.DataFrame(data)

category_column ="Indicateurs"


data=pd.read_csv("data3.csv")
categories_to_plot = ['Agriculture, forêt et pêche', 'Industrie','Bâtiments et travaux publics','Commerce de gros et de détail','Transports, entrepôts et communications ',' Services+Administration générale']
filtered_df = data[data[category_column].isin(categories_to_plot)]


# Prepare the data for plotting
years = [col for col in data.columns if col != 'Indicateurs']
source = ColumnDataSource(data={
    'year': years,
    **{cat: filtered_df[filtered_df[category_column] == cat][years].values.flatten() for cat in categories_to_plot}
})

#Visualisation 6
p6 = figure(height=400, width=600, title="Comparaison du taux de chômage pour 2010 et 2020(National)",
           x_axis_label='Year', y_axis_label='Value', toolbar_location=None, tools="")

# Add a line renderer
p6.line(x=df["Year"], y=df["Value"], line_width=2, color="navy", legend_label="Values")

# Add circle markers at each data point
p6.circle(x=df["Year"], y=df["Value"], size=10, color="red", legend_label="Values")

# Customize the plot
p6.legend.location = "top_left"
p6.xaxis.ticker = [2010, 2020]

#
category_column ="Indicateurs"


data=pd.read_csv("data3.csv")
categories_to_plot = ['Agriculture, forêt et pêche', 'Industrie','Bâtiments et travaux publics','Commerce de gros et de détail','Transports, entrepôts et communications ',' Services+Administration générale']
filtered_df = data[data[category_column].isin(categories_to_plot)]


# Prepare the data for plotting
years = [col for col in data.columns if col != 'Indicateurs']
source = ColumnDataSource(data={
    'year': years,
    **{cat: filtered_df[filtered_df[category_column] == cat][years].values.flatten() for cat in categories_to_plot}
})

#Visualisation 7
p7 = figure(title="Category Values Over Years", x_axis_label='Year', y_axis_label='Value')

# Add lines for each category
p7.line(x='year', y='Agriculture, forêt et pêche', source=source, legend_label='Agriculture, forêt et pêche', line_width=2, color='blue')
p7.line(x='year', y='Industrie', source=source, legend_label='Industrie', line_width=2, color='brown')
p7.line(x='year', y='Bâtiments et travaux publics', source=source, legend_label='Bâtiments et travaux publics', line_width=2, color='red')
p7.line(x='year', y='Commerce de gros et de détail', source=source, legend_label='Commerce de gros et de détail', line_width=2, color='green')
p7.line(x='year', y='Transports, entrepôts et communications', source=source, legend_label='Transports, entrepôts et communications', line_width=2, color='yellow')
p7.line(x='year', y=' Services+Administration générale', source=source, legend_label=' Services+Administration générale', line_width=2, color='black')

#Visualisation 8
p8 = figure(x_range=years, title="Category Values Over Years", x_axis_label='Year', y_axis_label='Value', 
           height=400, width=800)


# Add bars for each category
colors = ['blue', 'green','red','yellow','brown','black']  # Add more colors if needed
width = 0.15

for idx, cat in enumerate(categories_to_plot):
    p8.vbar(x=dodge('year', -width/2 + idx*width, range=p8.x_range), top=cat, width=width, source=source, 
           legend_label=cat, color=colors[idx % len(colors)])

# Customize the plot
p8.legend.title = 'Categories'
p8.legend.location = 'top_left'
p8.legend.label_text_font_size = '5pt'  
p8.xgrid.grid_line_color = None
p8.y_range.start = 0

#


#Visualisation 9
# Define the categories to plot
categories_to_plot = ['Sans diplôme(u)', 'Niveau moyen(u)', 'Niveau supérieur(u)', 
                      'Ayant un diplôme(u)', 'Sans diplôme(r)', 'Ayant un diplôme(r)']

# Filter the DataFrame
filtered_df1 = data[data[category_column].isin(categories_to_plot)]

# Define x and y values for the heatmap
x = [str(col) for col in filtered_df1.columns[1:]]  # Exclude the first column which contains the y-axis values
y = filtered_df1[category_column]

# Convert DataFrame values to a numpy array for the heatmap
values = filtered_df1.iloc[:, 1:].values.astype(float)

# Create a LinearColorMapper to map values to colors using the reversed 'RdYlBu' palette
colors = ["#006837", "#1a9850", "#66bd63", "#a6d96a", "#d9ef8b", "#ffffbf", "#fee08b", "#fdae61", "#f46d43", "#d73027"]
mapper = LinearColorMapper(palette=colors, low=np.min(values), high=np.max(values))

# Prepare the data source for the plot
source = ColumnDataSource(data={
    'x': np.repeat(x, len(y)),
    'y': np.tile(y, len(x)),
    'values': values.flatten()
})

# Create a Bokeh figure
p9 = figure(x_range=list(x), y_range=list(y[::-1]), height=400, width=800,
           title="Heatmap", toolbar_location=None, tools="hover", tooltips=[("value", "@values")])

# Plot the heatmap using Rect glyph
p9.rect(x="x", y="y", width=1, height=1, source=source,
       fill_color={'field': 'values', 'transform': mapper}, line_color=None)

# Customize the plot
p9.xaxis.axis_label = 'Year'
p9.yaxis.axis_label = 'Category'
p9.axis.major_label_text_font_size = "10pt"
p9.axis.axis_line_color = None
p9.axis.major_tick_line_color = None
p9.axis.minor_tick_line_color = None
p9.grid.grid_line_color = None

####
layout = gridplot([[p1, p2, p3, p4, p5, p6, p7, p8, p9]])
show(layout, notebook_handle=True)




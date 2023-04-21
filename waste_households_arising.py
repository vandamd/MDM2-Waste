import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("Waste_Data/waste_data.xlsx")

# Open sheet called "Waste from Households"
df = pd.read_excel(xlsx, "Waste from Households")

# Rename Relevant Columns
df = df.rename(columns={'Waste from Households, UK and country split, 2010-20':'Year', 'Unnamed: 1':'Measure', 'Unnamed: 2':'UK', 'Unnamed: 3':'England', 'Unnamed: 4':'NI', 'Unnamed: 5':'Scotland', 'Unnamed: 6':'Wales'})

# Filter the data to show only the 'Arisings' column
df = df[df['Measure'] == "Arisings"]

# Read population data from file 'population_uk.csv'
df_pop = pd.read_csv("Waste_Data/population_uk.csv")

# Delete the column called "ladcode20", 'sex' and 'age' from the population data
df_pop = df_pop.drop("ladcode20", axis=1)
df_pop = df_pop.drop("sex", axis=1)
df_pop = df_pop.drop("age", axis=1)
df_pop = df_pop.drop("Unnamed: 25", axis=1)

# Delete the "population_2001" - "population_2015" columns from the population data, columns 3-18
df_pop = df_pop.drop(df_pop.iloc[:, 2:17], axis=1)

# In a new df, create columns for 'Year', 'Country' and 'Total Population'
df_pop_f = pd.DataFrame(columns=['Year', 'Country', 'Total Population'])

countries = ['E', 'W', 'S', 'N']
years = ['2016', '2017', '2018', '2019', '2020']

# For each country calculate the sum of values in the 'population_20xx' column, from 2016 to 2020 and add to df_pop_f with the year, country and total population
for country in countries:
    for year in years:
        # Filter 'country' column 
        df_temp = df_pop[df_pop['country'] == country]
        df_pop_f = pd.concat([df_pop_f, pd.DataFrame({'Year': year, 'Country': country, 'Total Population': df_temp['population_' + year].sum()}, index=[0])], ignore_index=True)

# Rearrange the df so that it's 'Year', 'Country' and 'Tonnes'
df_rearr = pd.DataFrame(columns=['Year', 'Country', 'Tonnes'])

years = [2016, 2017, 2018, 2019, 2020]
countries = ['England', 'NI', 'Scotland', 'Wales']

for country in countries:
    for year in years:
        waste = df[df['Year'] == year][country]
        waste = int(waste)
        df_rearr = pd.concat([df_rearr, pd.DataFrame({'Year': year, 'Country': country, 'Tonnes': waste}, index=[0])], ignore_index=True)

# Multiply each value in tonnes by 1000
df_rearr['Tonnes'] = df_rearr['Tonnes'] * 1000

# Copy the df_rearr to a new df
df_norm = df_rearr.copy()

# Rename 'Tonnes' column to 'Tonnes per person'
df_norm = df_norm.rename(columns={'Tonnes':'Tonnes per person'})

tonnes = df_rearr['Tonnes']
population = df_pop_f['Total Population']

# Divide the tonnes by the population
df_norm['Tonnes per person'] = tonnes / population

# Create a plotly figure
fig2 = go.Figure()

# Add a trace for each country
for country in df_norm['Country'].unique():
    fig2.add_trace(
        go.Scatter(x=df_norm['Year'], y=df_norm[df_norm['Country'] == country]['Tonnes per person'], name=country)
    )

# Create a plotly figure (normalised)
fig = go.Figure()

# Add a trace for each country
for country in df.columns[2:]:
    fig.add_trace(
        go.Scatter(x=df['Year'], y=df[country]*1000, name=country)
    )

# Add title and axis labels
fig.update_layout(
    title="Arisings from Households in the UK",
    xaxis_title="Year",
    yaxis_title="Tonnes"
)

fig2.update_layout(
    title="Arisings from Households per person in the UK",
    xaxis_title="Year",
    yaxis_title="Tonnes per person"
)

# Update hover to show "Year" and "Thousand Tonnes"
fig.update_traces(hovertemplate="Tonnes %{y}")

# White background, grey gridlines
fig.update_layout(
    hovermode='x unified',
    plot_bgcolor='white',
    title_x=0.5,
    title_y=0.88,
    xaxis=dict(
        gridcolor='LightGrey',
        nticks=5
    ),
    yaxis=dict(
        gridcolor='LightGrey'
    )
)

fig2.update_layout(
    hovermode='x unified',
    plot_bgcolor='white',
    title_x=0.5,
    title_y=0.88,
    xaxis=dict(
        gridcolor='LightGrey',
        nticks=5
    ),
    yaxis=dict(
        gridcolor='LightGrey'
    )
)

# Better images
config = {
  'toImageButtonOptions': {
    'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'custom_image',
    'height': 575,
    'width': 796,
    'scale':10 # Multiply title/legend/axis/canvas sizes by this factor
  }
}

# Show the figure
fig.show(config=config)
fig2.show(config=config)
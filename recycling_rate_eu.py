"""
This script creates a plotly figure that shows the recycling rate in Europe from 2000 to 2019.
The data is taken from the Eurostat website.
"""

import pandas as pd
import plotly.graph_objects as go

# Read data from 'waste_gen_eu.tsv'
df = pd.read_csv("Waste_Data/recycling_rate_eu.tsv", sep="\t")

# Replace ':' with '0'
df = df.replace(': ', '0')

# Remove letters from columns B-J and rows 2 onwards
df.iloc[1:, 1:] = df.iloc[1:, 1:].replace('[a-zA-Z]', '', regex=True)

# Rename 'freq,unit,hazard,nace_r2,waste,geo\TIME_PERIOD' to 'category/country'
df = df.rename(columns={'freq,waste,unit,geo\TIME_PERIOD':'country'})

df = df[df['country'].str.contains('W1501,')]

# Each element in 'category/country' looks like 'A,W1501,RT,AT'. We want to keep the country code found at the end
df['country'] = df['country'].str.split(",").str[-1]

# Create a dictionary that maps country codes to country names
country_names = {
    'AT': 'Austria',
    'BA': 'Bosnia and Herzegovina',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'EL': 'Greece',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IS': 'Iceland',
    'IT': 'Italy',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'ME': 'Montenegro',
    'MK': 'North Macedonia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'TR': 'Turkey',
    'UK': 'United Kingdom',
    'XK': 'Kosovo'
}

# Replace the country codes in the 'country' column with their respective names
df['country'] = df['country'].replace(country_names)

# Filter for the countries we want to keep, United Kingdom, Spain, France, Italy, Germany
df = df[df['country'].isin(['United Kingdom', 'Spain', 'France', 'Italy', 'Germany'])]

# Convert the values in the year columns to numeric
df[df.columns[1:]] = df[df.columns[1:]].apply(pd.to_numeric)

# Create a plotly figure
fig = go.Figure()

# Loop through each country in the dataframe, if the value is 0 then set it to None
for country in df['country'].unique():
    # Filter the dataframe for the current country
    df_country = df[df['country'] == country]
    # Add a line trace for the current country
    fig.add_trace(
        go.Scatter(x=df.columns[1:], y=df_country.iloc[0, 1:].replace(0, None), name=country)
    )

# Set the x-axis title
fig.update_xaxes(title_text='Year')

# Set the y-axis title
fig.update_yaxes(title_text='Recycling Rate (%)')

# Improve readability of the hover labels, no decimals
fig.update_traces(hovertemplate='%{y}%')

fig.update_layout(title_text='Recycling Rate by Country in Europe')

# White background, grey gridlines
fig.update_layout(
    hovermode='x unified',
    plot_bgcolor='white',
    title_x=0.5,
    title_y=0.88,
    xaxis=dict(
        gridcolor='LightGrey'
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
"""
This script creates an animated bubble map of the remaining capacity of inert landfills in England using Plotly and mapbox.
The data is taken from the Environment Agency website.
"""

import pandas as pd
from geopy.geocoders import Nominatim
import requests
import plotly.express as px

# Create a new spreadsheet with the same columns as the first sheet
df = pd.read_excel("Landfill_Data/2015_Landfill_Capacity.xlsx", "Landfill Capacity-England 2015")
df = df.rename(columns={'Facility address':'addresses','Landfill Site type':'landfill type','Remaining Capacity end (cubic metres)':'remaining capacity'})

# Delete columns that are not needed
df = df.drop(df.columns[[0, 1, 2, 4, 5, 6, 7]], axis=1)

# Create a new column for the year
df['year'] = 2015

# Loop through the remaining sheets and append them to the new spreadsheet, adding their respective year between 2016 and 2018
for year in range(2016, 2018):
    df2 = pd.read_excel("Landfill_Data/" + str(year) + "_Landfill_Capacity.xlsx", "Landfill Capacity-England " + str(year))
    # rename columns, remaining capacity column name changes each year
    df2 = df2.rename(columns={'Facility address':'addresses','Landfill Site type':'landfill type','Remaining Capacity end (cubic metres)':'remaining capacity'})
    df2 = df2.drop(df2.columns[[0, 1, 2, 4, 5, 6, 7]], axis=1)
    df2['year'] = year
    df = pd.concat([df, df2], ignore_index=True)

# Loop through the remaining sheets and append them to the new spreadsheet, adding their respective year between 2016 and 2018
for year in range(2018, 2022):
    df2 = pd.read_excel("Landfill_Data/" + str(year) + "_Landfill_Capacity.xlsx", "Landfill Capacity-England " + str(year))
    # rename columns, remaining capacity column name changes each year
    df2 = df2.rename(columns={'Facility Address':'addresses','Site Type':'landfill type','Remaining Capacity end (cubic metres)':'remaining capacity'})
    df2 = df2.drop(df2.columns[[0, 1, 2, 4, 5, 6, 7]], axis=1)
    df2['year'] = year
    df = pd.concat([df, df2], ignore_index=True)

# Delete the rows with 'Closed' in the 'remaining capacity' column
df = df[df['remaining capacity'].isin(['Closed']) == False]

# Create two new columns, one for the latitude and one for the longitude
df['latitude'] = 0
df['longitude'] = 0

# Create a postcode column
df['postcode'] = 0

# Filter landfill type for 'Inert Landfill', 'L05 - Inert Landfill'
df = df[df['landfill type'].isin(['Inert Landfill', 'L05 - Inert Landfill', 'L05: Inert Landfill'])]

# Extract the postcodes from the addresses using a regular expression
df['postcode'] = df['addresses'].str.extract('([A-Z]{1,2}[0-9][A-Z0-9]? [0-9][A-Z]{2})', expand=True)

# Remove the rows with no postcode
df = df[df['postcode'].isnull() == False]

# List of postcodes
postcodes = df['postcode'].tolist()

# Using Postcodes.io API to get the latitude and longitude of each postcode
url = "https://api.postcodes.io/postcodes"

# Use the list of postcodes to query the url in batches of 100
for i in range(0, len(postcodes), 100):
    batch = postcodes[i:i+100]
    response = requests.post(url, json={"postcodes": batch})
    data = response.json()

    # print('\n')
    # pprint.pprint(data['result'])

    # Loop through the results and add the latitude and longitude to the spreadsheet
    for result in data['result']:
        # If result is 'none' then skip
        if result['result'] is None:
            continue

        df.loc[df['postcode'] == result['query'], 'latitude'] = result['result']['latitude']
        df.loc[df['postcode'] == result['query'], 'longitude'] = result['result']['longitude']

# Remove the rows with a latitude or longitude of 0
df = df[df['latitude'] != 0]

# Remove the rows with a remaining capacity of 0
# df = df[df['remaining capacity'] != 0]

# Convert the remaining capcity and year columns to numeric
df['remaining capacity'] = pd.to_numeric(df['remaining capacity'], errors='coerce')
df['year'] = pd.to_numeric(df['year'])

# Remove the rows with an invalid remaining capacity
df = df[df['remaining capacity'].isnull() == False]

# Create an animated bubble map of the remaining capacity of inert landfills in England using Plotly and mapbox
fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                        color="remaining capacity",
                        size="remaining capacity",
                        animation_frame="year",
                        mapbox_style="carto-positron",
                        zoom=5.5,
                        center={"lat": 52.930427, "lon": -1.710752},
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
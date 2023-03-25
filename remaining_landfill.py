import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from requests.structures import CaseInsensitiveDict

# Read data from file '2015 Remaining Landfill capacity - England.xlsx'
xlsx = pd.ExcelFile("2015_Remaining_Landfill_capacity_England.xlsx")

# Open sheet called "Landfill Capacity-England 2015"
df = pd.read_excel(xlsx,"Landfill Capacity-England 2015")

# Rename Relevant Columns
df = df.rename(columns={'Unnamed: 3':'addresses','Unnamed: 8':'landfill type','Unnamed: 9':'remaining capacity'})

# Convert 'remaining capacity' column to numeric
df['remaining capacity'] = pd.to_numeric(df['remaining capacity'], errors='coerce')

# Remove rows with missing or invalid values in 'remaining capacity' column
df = df.dropna(subset=['remaining capacity'])

# Filter the data to show only the total waste generation
df = df[df['landfill type'] == "Inert Landfill"]

# Replace closed with 0
df['remaining capacity'] = df['remaining capacity'].replace('Closed',0)

addresses = df['addresses']

# Generate longitude and latitude values for the corresponding addresses
longitude = []
latitude = []

for i in addresses:
    url = "https://api.geoapify.com/v1/geocode/search?text={" + str(i) +"}&apiKey=66a72e32bdb64ef6992f0ae20f27922b"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        data = resp.json()
        if len(data['features']) > 0:
            lat = data['features'][0]['properties']['lat']
            long = data['features'][0]['properties']['lon']
            longitude.append(long)
            latitude.append(lat)
        else:
            print('No results found for', i)
            # Remove the landfill sites whose coordinates are not found
            df = df.drop(index=df[df['addresses']==i].index)
                
    else:
        print(f'Request failed with status code {response.status_code}.')

print(latitude)
print(longitude)

# Mapbox plot
fig = px.scatter_mapbox(df,
                        lon = longitude,
                        lat = latitude,
                        zoom = 5,
                        size = df['remaining capacity'],
                        width = 1200,
                        height = 900,
                        title = 'Remaining Landfill Capacity - 2015'
                        )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":10})
fig.show()
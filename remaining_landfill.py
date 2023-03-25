import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from addresses import longlat

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

[longitude, latitude]=longlat(df,addresses)

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
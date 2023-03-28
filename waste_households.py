import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("data/waste_data.xlsx")

# Open sheet called "Waste from Households"
df = pd.read_excel(xlsx, "Waste from Households")

# Rename Relevant Columns
df = df.rename(columns={'Waste from Households, UK and country split, 2010-20':'Year', 'Unnamed: 1':'Measure', 'Unnamed: 2':'UK', 'Unnamed: 3':'England', 'Unnamed: 4':'NI', 'Unnamed: 5':'Scotland', 'Unnamed: 6':'Wales'})

# Filter the data to show only the 'Recycling rate (incl. IBAm)' in the 'Measure' column
df = df[df['Measure'] == "Recycling rate (incl. IBAm)"]

# Create a plotly figure
fig = go.Figure()

# Add a trace for each country
for country in df.columns[2:]:
    fig.add_trace(
        go.Scatter(x=df['Year'], y=df[country]*100, name=country)
    )

# Add title and axis labels
fig.update_layout(
    title="Recycling Rate from Households in the UK",
    xaxis_title="Year",
    yaxis_title="Recycling Rate (%)"
)

# Update hover to show "Year" and "Recycling Rate (%)"
fig.update_traces(hovertemplate="Year: %{x}<BR>Recycling Rate: %{y:.2f}%")

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
import pandas as pd
import plotly.graph_objects as go

# Read data from file 'constructionsannualtables2021.xlsx'
xlsx = pd.ExcelFile("Waste_Data/constructionsannualtables2021.xlsx")

# Open sheet called "Table 1.3"
df = pd.read_excel(xlsx, "Table 1.3")

# Rename Relevant Columns
df = df.rename(columns={'Unnamed: 20':'Total Work'})

# Filter df to show row 5-28
df = df.iloc[5:29]

# Create a plotly figure
fig = go.Figure()

# Create a plotly line graph for the Total Work
fig.add_trace(
    go.Scatter(x=df['Year'], y=df['Total Work'], name="Total Work")
)

# Update layout properties
fig.update_layout(
    title="Value of construction output in the UK",
    xaxis_title="Year",
    yaxis_title="Current prices (£ million)",
)

# Show all x-axis ticks
fig.update_xaxes(
    tickmode = 'linear',
    tick0 = 2010,
    dtick = 2
)

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
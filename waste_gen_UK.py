import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("Waste_Data/waste_data.xlsx")

# Open sheet called "Waste Gen Eng 2010-18"
UK_df = pd.read_excel(xlsx, "Waste Gen UK 2010 -18")

# Rename Relevant Columns
UK_df = UK_df.rename(columns={'Total generation of waste, split by NACE economic activity and EWC-STAT waste material, 2010-2018, UK':'Year', 'Unnamed: 1':'EWC-STAT code', 'Unnamed: 21':'Total waste generation', 'Unnamed: 3':'Hazardous/Non-hazardous split'})

# Filter EWC-STAT code to show only 'Total'
UK_df = UK_df[UK_df['EWC-STAT code'] == "Total"]

# Filter hazardous/non-hazardous split to show only 'Total'
UK_df = UK_df[UK_df['Hazardous/Non-hazardous split'] == "Total"]

# Create a plotly figure
fig = go.Figure()

# Create a plotly line graph for the total waste generation
fig.add_trace(
    go.Scatter(x=UK_df['Year'], y=UK_df['Total waste generation'], name="Total waste generation")
)

# Update layout properties
fig.update_layout(
    title="Total waste generation in the UK",
    xaxis_title="Year",
    yaxis_title="Total waste generation (tonnes)",
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
import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("waste_data.xlsx")

# Open sheet called "Waste Gen Eng 2010-18"
df = pd.read_excel(xlsx, "Packaging")

# Delete rows 1 to 6
df = df.drop(df.index[0:6])

# Rename Relevant Columns
df = df.rename(columns={'Packaging waste and recycling / recovery, split by material, UK 2012-20':'Year', 'Unnamed: 1':'Material', 'Unnamed: 4':'Recycling Rate'})

# Create a plotly figure
fig = go.Figure()

# Add a trace for each material type
for material in df['Material'].unique():
    fig.add_trace(
        go.Scatter(x=df[df['Material'] == material]['Year'], y=df[df['Material'] == material]['Recycling Rate']*100, name=material)
    )

# Update layout properties
fig.update_layout(
    title="Recycling Rate of Packaging Waste in the UK",
    xaxis_title="Year",
    yaxis_title="Recycling Rate (%) / Achieved Recovery",
)

# Hover to show "Year" and "Recycling Rate (%)"
fig.update_traces(hovertemplate="Year: %{x}<BR>Recycling Rate: %{y:.2f}%")

# Show the figure
fig.show()
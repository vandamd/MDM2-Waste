# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 10:37:34 2023

@author: judah
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default ='browser'

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("waste_data.xlsx")

# Open sheet called "Waste Gen Eng 2010-18"
df = pd.read_excel(xlsx, "Packaging")

# Rename Relevant Columns
df = df.rename(columns={'Packaging waste and recycling / recovery, split by material, UK 2012-20':'Year', 'Unnamed: 1':'Materials', 'Unnamed: 2':'packaging waste'})

# Replace z with 0
df = df.replace('z', 0)

# Filter the data to only show Total recycling in Material
df = df[df['Materials'] == "Total recycling"]

# Create a plotly figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=df['Year'], y=df['packaging waste'])
)

# Define the dropdown menus
# dropdown_buttons = [
#     dict(
#         args=[{"visible": [trace.stackgroup == desc for trace in fig.data]}],
#         label=desc,
#         method="update",
#     )
#     for desc in df['Materials'].unique()
# ]

# pop last element from dropdown_buttons
# dropdown_buttons.pop(-1)

# Update layout properties
# fig.update_layout(
#     title_text="Packaging Waste",
#     updatemenus=[
#         dict(
#             buttons=dropdown_buttons,
#             direction="down",
#             # Make the dropdown show below the title
#             x=0,
#             xanchor="left",
#             y=1.07,
#             yanchor="top",
#             pad={"r": 10, "t": 10},
#             showactive=True,
#         ),
#     ]
# )


# Add title to x-axis
fig.update_xaxes(title_text="Year")

# Add title to y-axis
fig.update_yaxes(title_text="Total Packaging Waste (tonnes)")

# Improve readability of the hover text
fig.update_traces(hovertemplate="<b>%{y}</b> tonnes")

# Add marker to data points
fig.update_traces(mode='markers+lines')

# Show figure
fig.show()
    

        
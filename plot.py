import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("waste_data.xlsx")

# Open sheet called "Waste Gen Eng 2010-18"
england_df = pd.read_excel(xlsx, "Waste Gen Eng 2010-18")

# Rename Relevant Columns
england_df = england_df.rename(columns={'Total generation of waste, split by NACE economic activity and EWC-STAT waste material, 2010-2018, England':'Year', 'Unnamed: 2':'EWC-STAT description', 'Unnamed: 21':'Total waste generation', 'Unnamed: 3':'Hazardous/Non-hazardous split'})

# Read columns A, C, D, V
england_df = england_df[['Year', 'EWC-STAT description', 'Total waste generation', 'Hazardous/Non-hazardous split']]

# Replace z with 0
england_df = england_df.replace('z', 0)

# Create a plotly figure
fig = go.Figure()

# Add line traces for each EWC-STAT description and hazardous/non-hazardous split
for ewc in england_df['EWC-STAT description'].unique():
    for split in ["Hazardous", "Non-hazardous"]:
        ewc_df = england_df[(england_df['EWC-STAT description'] == ewc) & (england_df['Hazardous/Non-hazardous split'] == split)]
        fig.add_trace(
            go.Scatter(x=ewc_df['Year'], y=ewc_df['Total waste generation'], name=f"{split} - {ewc}", visible=False)
        )

# Set the visibility of the first two traces to True
fig.data[0].visible = True
fig.data[1].visible = True

# Define the dropdown menus
dropdown_buttons = [
    dict(
        args=[{"visible": [trace.name == f"{split} - {desc}" for trace in fig.data for split in ["Hazardous", "Non-hazardous"]]}],
        label=desc,
        method="update",
    )
    for desc in england_df['EWC-STAT description'].unique()
]

# Update the visibility settings for the dropdown buttons
for i, desc in enumerate(england_df['EWC-STAT description'].unique()):
    visible_list = [False] * len(fig.data)
    visible_list[i * 2] = True
    visible_list[i * 2 + 1] = True
    dropdown_buttons[i]['args'][0]['visible'] = visible_list

# pop the first two items from the dropdown menu
dropdown_buttons.pop(0)
dropdown_buttons.pop(0)

# pop the last item
dropdown_buttons.pop(-1)

# Update layout properties
fig.update_layout(
    title_text="Waste Generation in England",
    updatemenus=[
        dict(
            buttons=dropdown_buttons,
            direction="down",
            x=0.5,
            xanchor="center",
            y=1.1,
            yanchor="top",
        )
    ]
)

# Add title to x-axis
fig.update_xaxes(title_text="Year")

# Add title to y-axis
fig.update_yaxes(title_text="Total Waste Generation (tonnes)")

# Improve readability of the hover text
fig.update_traces(hovertemplate="<b>%{y}</b> tonnes")

# Remove k from the y-axis tick labels
fig.update_yaxes(tickformat=",")

# Show plot
fig.show()
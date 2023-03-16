import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("waste_data.xlsx")

# Open sheet called "Waste Gen Eng 2010-18"
england_df = pd.read_excel(xlsx, "Waste Gen Eng 2010-18")

# Rename Relevant Columns
england_df = england_df.rename(columns={'Total generation of waste, split by NACE economic activity and EWC-STAT waste material, 2010-2018, England':'Year', 'Unnamed: 2':'EWC-STAT description', 'Unnamed: 21':'Total waste generation', 'Unnamed: 3':'Hazardous/Non-hazardous split'})

# Rename NACE columns
nace_columns = {
    'Unnamed: 4': 'A',
    'Unnamed: 5': 'B',
    'Unnamed: 6': 'C10-C12',
    'Unnamed: 7': 'C13-C15',
    'Unnamed: 8': 'C16',
    'Unnamed: 9': 'C17_C18',
    'Unnamed: 10': 'C19',
    'Unnamed: 11': 'C20-C22',
    'Unnamed: 12': 'C23',
    'Unnamed: 13': 'C24_C25',
    'Unnamed: 14': 'C26-C30',
    'Unnamed: 15': 'C31-C33',
    'Unnamed: 16': 'D',
    'Unnamed: 17': 'E36_E37_E39',
    'Unnamed: 18': 'F',
    'Unnamed: 19': 'G-U_X_G4677',
    'Unnamed: 20': 'EP_HH'
}

england_df = england_df.rename(columns=nace_columns)

# Filter the data to show only the total waste generation
england_df = england_df[england_df['Hazardous/Non-hazardous split'] == "Total"]

# Replace z with 0
england_df = england_df.replace('z', 0)

# Create a plotly figure
fig = go.Figure()

# Add area traces for each NACE code and EWC-STAT description
for nace_code in nace_columns.values():
    for ewc in england_df['EWC-STAT description'].unique():
        ewc_df = england_df[(england_df['EWC-STAT description'] == ewc)].pivot_table(index='Year', columns='EWC-STAT description', values=nace_code).reset_index()
        sum_values = ewc_df.iloc[:, 1:].sum(axis=1)
        if sum_values.sum() > 0:
            fig.add_trace(
                go.Scatter(x=ewc_df['Year'], y=sum_values, name=f"{nace_code} - {ewc}", stackgroup=ewc, mode='lines', line_shape='spline', visible=(ewc == "Total"))
            )

# Define the dropdown menus
dropdown_buttons = [
    dict(
        args=[{"visible": [trace.stackgroup == desc for trace in fig.data]}],
        label=desc,
        method="update",
    )
    for desc in england_df['EWC-STAT description'].unique()
]

# pop last element from dropdown_buttons
dropdown_buttons.pop(-1)

# Update layout properties
fig.update_layout(
    title_text="Waste Generation in England by NACE Code and EWC-STAT Description",
    updatemenus=[
        dict(
            buttons=dropdown_buttons,
            direction="down",
            # Make the dropdown show below the title
            x=0,
            xanchor="left",
            y=1.07,
            yanchor="top",
            pad={"r": 10, "t": 10},
            showactive=True,
        ),
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

# Add marker to data points
fig.update_traces(mode='markers+lines')

# Show plot
fig.show()
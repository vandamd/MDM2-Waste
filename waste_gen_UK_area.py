import pandas as pd
import plotly.graph_objects as go

# Read data from file 'waste_data.xlsx'
xlsx = pd.ExcelFile("Waste_Data/waste_data.xlsx")

# Open sheet called "Waste Gen Eng 2010-18"
UK_df = pd.read_excel(xlsx, "Waste Gen UK 2010 -18")

# Rename Relevant Columns
UK_df = UK_df.rename(columns={'Total generation of waste, split by NACE economic activity and EWC-STAT waste material, 2010-2018, UK':'Year', 'Unnamed: 1':'EWC-STAT code', 'Unnamed: 21':'Total waste generation', 'Unnamed: 3':'Hazardous/Non-hazardous split'})

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

# nace_columns = {
#     'Unnamed: 4': 'A - Agriculture, forestry and fishing',
#     'Unnamed: 5': 'B - Mining and quarrying',
#     'Unnamed: 6': 'C10-C12 - Food products, beverages and tobacco',
#     'Unnamed: 7': 'C13-C15 - Textiles, wearing apparel and leather products',
#     'Unnamed: 8': 'C16 - Wood and of products of wood and cork, except furniture; articles of straw and plaiting materials',
#     'Unnamed: 9': 'C17_C18 - Paper and paper products; printing and reproduction of recorded media',
#     'Unnamed: 10': 'C19 - Coke and refined petroleum products',
#     'Unnamed: 11': 'C20-C22 - Chemical, pharmaceutical, rubber and plastic products',
#     'Unnamed: 12': 'C23 - Non-metallic mineral products',
#     'Unnamed: 13': 'C24_C25 - Basic metals and fabricated metal products, except machinery and equipment',
#     'Unnamed: 14': 'C26-C30 - Computer, electronic and optical products, electrical equipment, motor vehicles and other transport equipment',
#     'Unnamed: 15': 'C31-C33 - Furniture, jewellery, musical instruments, toys, repair and installation or machinery and equipment',
#     'Unnamed: 16': 'D - Electricity, gas, steam and air conditioning supply',
#     'Unnamed: 17': 'E36_E37_E39 - Water collection, treatment and supply, sewerage, remediation activities and other waste management services',
#     'Unnamed: 18': 'F - Construction',
#     'Unnamed: 19': 'G-U_X_G4677 - Services (except wholesale of waste and scrap)',
#     'Unnamed: 20': 'EP_HH - Households'
# }

UK_df = UK_df.rename(columns=nace_columns)

# Filter EWC-STAT code to show only 'Total'
UK_df = UK_df[UK_df['EWC-STAT code'] == "Total"]

# Filter hazardous/non-hazardous split to show only 'Total'
UK_df = UK_df[UK_df['Hazardous/Non-hazardous split'] == "Total"]

# Create a plotly figure
fig = go.Figure()

# Add area traces for each NACE code
for nace_code in nace_columns.values():
    for ewc in UK_df['EWC-STAT code'].unique():
        ewc_df = UK_df[(UK_df['EWC-STAT code'] == ewc)].pivot_table(index='Year', columns='EWC-STAT code', values=nace_code).reset_index()
        sum_values = ewc_df.iloc[:, 1:].sum(axis=1)
        if sum_values.sum() > 0:
            fig.add_trace(
                go.Scatter(x=ewc_df['Year'], y=sum_values, name=f"{nace_code} - {ewc}", stackgroup=ewc, mode='lines', line_shape='spline', visible=(ewc == "Total"))
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
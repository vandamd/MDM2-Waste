import pandas as pd
import plotly.graph_objects as go

# Read data from 'waste_gen_eu.tsv'
df = pd.read_csv("Waste_Data/population_eu.tsv", sep="\t")

# Replace ':' with '0'
df = df.replace(': ', '0')

# Replace ': c' with '0'
df = df.replace(': c', '0')

# Remove letters from columns B-J and rows 2 onwards
df.iloc[0:, 1:13] = df.iloc[0:, 1:13].replace('[a-zA-Z]', '', regex=True)

# Replace ':' with '0'
df = df.replace(': ', '0')

# Rename 'freq,indic_de,geo\TIME_PERIOD' to 'country'
df = df.rename(columns={'freq,indic_de,geo\TIME_PERIOD':'country'})

# Keep the last two characters of each element in 'country'
df['country'] = df['country'].str[-2:]

# Rename the country names, DE, ES, FR, IT, UK
df = df.replace({'country': {'DE': 'Germany', 'ES': 'Spain', 'FR': 'France', 'IT': 'Italy', 'UK': 'United Kingdom'}})

# Replace 0 with NaN
df = df.replace('0', pd.NA)

# Create a plotly figure
fig = go.Figure()

# Add a trace for each country with markers
fig.add_trace(go.Scatter(x=df.columns[1:], y=df.iloc[0, 1:], name='Germany'))
fig.add_trace(go.Scatter(x=df.columns[1:], y=df.iloc[1, 1:], name='Spain'))
fig.add_trace(go.Scatter(x=df.columns[1:], y=df.iloc[2, 1:], name='France'))
fig.add_trace(go.Scatter(x=df.columns[1:], y=df.iloc[3, 1:], name='Italy'))
fig.add_trace(go.Scatter(x=df.columns[1:], y=df.iloc[4, 1:], name='United Kingdom'))

# Update layout properties
fig.update_layout(
    title="Population of European countries",
    xaxis_title="Year",
    yaxis_title="Population",
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
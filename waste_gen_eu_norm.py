import pandas as pd
import plotly.graph_objects as go

# Read data from 'waste_gen_eu.tsv'
popd = pd.read_csv("Waste_Data/population_eu.tsv", sep="\t")

# Replace ':' with '0'
popd = popd.replace(': ', '0')

# Replace ': c' with '0'
popd = popd.replace(': c', '0')

# Remove letters from columns B-J and rows 2 onwards
popd.iloc[0:, 1:13] = popd.iloc[0:, 1:13].replace('[a-zA-Z]', '', regex=True)

# Replace ':' with '0'
popd = popd.replace(': ', '0')

# Rename 'freq,indic_de,geo\TIME_PERIOD' to 'country'
popd = popd.rename(columns={'freq,indic_de,geo\TIME_PERIOD':'country'})

# Keep the last two characters of each element in 'country'
popd['country'] = popd['country'].str[-2:]

# Rename the country names, DE, ES, FR, IT, UK
popd = popd.replace({'country': {'DE': 'Germany', 'ES': 'Spain', 'FR': 'France', 'IT': 'Italy', 'UK': 'United Kingdom'}})

# Replace 0 with NaN
popd = popd.replace('0', pd.NA)


# Read data from 'waste_gen_eu.tsv'
gen = pd.read_csv("Waste_Data/waste_gen_eu.tsv", sep="\t")

# Only use the first 1000 rows
# gen = gen.head(2500)

# Replace ':' with '0'
gen = gen.replace(': ', '0')

# Replace ': c' with '0'
gen = gen.replace(': c', '0')

# Remove letters from columns B-J and rows 2 onwards
gen.iloc[1:, 1:10] = gen.iloc[1:, 1:10].replace('[a-zA-Z]', '', regex=True)

# Replace ':' with '0'
gen = gen.replace(': ', '0')

# Rename 'freq,unit,hazard,nace_r2,waste,geo\TIME_PERIOD' to 'category/country'
gen = gen.rename(columns={'freq,unit,hazard,nace_r2,waste,geo\TIME_PERIOD':'category/country'})

# Each element in 'category/country' looks like 'A,T,HAZ_NHAZ,A,PRIM,AT'. Let's remove 'A,T,HAZ_NHAZ'
gen['category/country'] = gen['category/country'].str[13:]

# Create a new column called 'country' and set it to the last element in 'category/country'
gen['country'] = gen['category/country'].str.split(",").str[-1]

# Create a new column called 'category' and set it to the first element in 'category/country'
gen['category'] = gen['category/country'].str.split(",").str[0]

# Create a new column called 'waste' and set it to the second element in 'category/country'
gen['waste'] = gen['category/country'].str.split(",").str[1]

# Delete the 'category/country' column
gen = gen.drop(columns=['category/country'])

# Move the 'waste' column to the front
gen = gen[['waste'] + [col for col in gen.columns if col != 'waste']]

# Move the 'category' column to the front
gen = gen[['category'] + [col for col in gen.columns if col != 'category']]

# Move the 'country' column to the front
gen = gen[['country'] + [col for col in gen.columns if col != 'country']]

# Filter for 'C20-C22'
gen = gen[gen['category'] == 'TOTAL_HH']

# Filter for W074
gen = gen[gen['waste'] == 'TOTAL']

# Remove extra spaces from the column names
gen.columns = gen.columns.str.strip()

# Create a dictionary that maps country codes to country names
country_names = {
    'AT': 'Austria',
    'BA': 'Bosnia and Herzegovina',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'EL': 'Greece',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IS': 'Iceland',
    'IT': 'Italy',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'ME': 'Montenegro',
    'MK': 'North Macedonia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'TR': 'Turkey',
    'UK': 'United Kingdom',
    'XK': 'Kosovo'
}

# Replace the country codes in the 'country' column with their respective names
gen['country'] = gen['country'].replace(country_names)

# Filter for the countries we want to keep, United Kingdom, Spain, France, Italy, Germany
gen = gen[gen['country'].isin(['United Kingdom', 'Spain', 'France', 'Italy', 'Germany'])]

# Convert the values in the year columns to numeric
gen[gen.columns[3:]] = gen[gen.columns[3:]].apply(pd.to_numeric)

# Delete columns in popd
popd = popd.drop(columns=['2011 ', '2013 ', '2015 ', '2017 ', '2019 ', '2021 ', '2022 '])

# Delete columns in gen
gen = gen.drop(columns=['2004', '2006', '2008', '2010', 'category', 'waste'])






# Create a normalised waste dataframe
popd_norm = popd.copy()

years = ['2012', '2014', '2016', '2018', '2020']

# Create a list of the population values for each country
popd_list = []

for i in range(0, len(popd)):
    popd_list.append(popd.iloc[i, 1:].tolist())
    # make sure values are floats
    popd_list[i] = [int(x) for x in popd_list[i]]

# Create a list of the waste values for each country
gen_list = []

for i in range(0, len(gen)):
    gen_list.append(gen.iloc[i, 2:].tolist())

gen_list[-1][-1] = 1

# Create a list of the normalised waste values for each country
waste_norm = []

# Calculate the normalised waste values for each country
for i in range(0, len(popd_list)):
    waste_norm.append([x / y for x, y in zip(gen_list[i], popd_list[i])])

waste_norm[-1][-1] = pd.NA

# Create a new df for normalised waste with year, country and waste columns
waste_norm_df = pd.DataFrame(columns=['year', 'country', 'waste per person'])


# Add the year, country and waste values to the new df
for i in range(0, len(waste_norm)):
    for j in range(0, len(waste_norm[i])):
        # Use concat instead of append to avoid a SettingWithCopyWarning
        waste_norm_df = pd.concat([waste_norm_df, pd.DataFrame([[years[j], popd.iloc[i, 0], waste_norm[i][j]]], columns=['year', 'country', 'waste per person'])])

# Create a plotly figure
fig = go.Figure()

# Add trace for each country
for country in waste_norm_df['country'].unique():
    fig.add_trace(go.Scatter(x=waste_norm_df[waste_norm_df['country'] == country]['year'], y=waste_norm_df[waste_norm_df['country'] == country]['waste per person'], name=country))

fig.update_layout(
    title="Waste generated per person by Country in Europe",
    xaxis_title="Year",
    yaxis_title="Tonnes per person"
)

# White background, grey gridlines
fig.update_layout(
    hovermode='x unified',
    plot_bgcolor='white',
    title_x=0.5,
    title_y=0.88,
    xaxis=dict(
        gridcolor='LightGrey',
        nticks=5
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
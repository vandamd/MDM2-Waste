import pandas as pd
from geopy.geocoders import Nominatim

# Create a new spreadsheet with the same columns as the first sheet
df = pd.read_excel("data/2015_Landfill_Capacity.xlsx", "Landfill Capacity-England 2015")
df = df.rename(columns={'Facility address':'addresses','Landfill Site type':'landfill type','Remaining Capacity end (cubic metres)':'remaining capacity'})

# Delete columns that are not needed
df = df.drop(df.columns[[0, 1, 2, 4, 5, 6, 7]], axis=1)

# Create a new column for the year
df['year'] = 2015

# Loop through the remaining sheets and append them to the new spreadsheet, adding their respective year between 2016 and 2018
for year in range(2016, 2018):
    df2 = pd.read_excel("data/" + str(year) + "_Landfill_Capacity.xlsx", "Landfill Capacity-England " + str(year))
    # rename columns, remaining capacity column name changes each year
    df2 = df2.rename(columns={'Facility address':'addresses','Landfill Site type':'landfill type','Remaining Capacity end (cubic metres)':'remaining capacity'})
    df2 = df2.drop(df2.columns[[0, 1, 2, 4, 5, 6, 7]], axis=1)
    df2['year'] = year
    df = df.append(df2, ignore_index=True)

# Loop through the remaining sheets and append them to the new spreadsheet, adding their respective year between 2016 and 2018
for year in range(2018, 2022):
    df2 = pd.read_excel("data/" + str(year) + "_Landfill_Capacity.xlsx", "Landfill Capacity-England " + str(year))
    # rename columns, remaining capacity column name changes each year
    df2 = df2.rename(columns={'Facility Address':'addresses','Site Type':'landfill type','Remaining Capacity end (cubic metres)':'remaining capacity'})
    df2 = df2.drop(df2.columns[[0, 1, 2, 4, 5, 6, 7]], axis=1)
    df2['year'] = year
    df = df.append(df2, ignore_index=True)

# Delete the rows with 'Closed' in the 'remaining capacity' column
df = df[df['remaining capacity'].isin(['Closed']) == False]

# Create two new columns, one for the latitude and one for the longitude
df['latitude'] = 0
df['longitude'] = 0

# print(df)

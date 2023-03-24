import pandas as pd
import plotly.graph_objects as go
import requests
from requests.structures import CaseInsensitiveDict

# Read data from file '2015 Remaining Landfill capacity - England.xlsx'
xlsx = pd.ExcelFile("2015_Remaining_Landfill_capacity_England.xlsx")

# Open sheet called "Remaining landfill capacity: England as at end 2015"
df = pd.read_excel(xlsx,"Remaining landfill capacity: England as at end 2015")

# Rename Relevant Columns
#df = df.rename(columns={'Unnamed: 4':'adresses','Unnamed: 9':'landfill type','Unnamed: 10':'remaining_capacity'})

# Filter the data to show only the total waste generation
#df = df[df['landfill type'] == "Inert Landfill"]

# Replace closed with 0
#df = df.replace('Closed',0)

print(df)

# Generate longitude and latitude values for the corresponding addresses
# longitude = []
# latitude = []

# for i in addresses:
#     url = "https://api.geoapify.com/v1/geocode/search?text={" + str(i) +"}&apiKey=66a72e32bdb64ef6992f0ae20f27922b"
#     print(url)

#     headers = CaseInsensitiveDict()
#     headers["Accept"] = "application/json"


#     resp = requests.get(url, headers=headers)

#     if resp.status_code == 200:
#         data = resp.json()
#         if len(data['features']) > 0:
#             lat = data['features'][0]['properties']['lat']
#             long = data['features'][0]['properties']['lon']
#             longitude.append(long)
#             latitude.append(lat)
#         else:
#             print('No results found.')
#     else:
#         print(f'Request failed with status code {response.status_code}.')

# print(latitude)
# print(longitude)

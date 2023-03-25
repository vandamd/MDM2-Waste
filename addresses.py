import requests
from requests.structures import CaseInsensitiveDict

# Generate longitude and latitude values for the corresponding addresses
def longlat(df,addresses):
    longitude = []
    latitude = []

    for i in addresses:
        url = "https://api.geoapify.com/v1/geocode/search?text={" + str(i) +"}&apiKey=66a72e32bdb64ef6992f0ae20f27922b"

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            data = resp.json()
            if len(data['features']) > 0:
                lat = data['features'][0]['properties']['lat']
                long = data['features'][0]['properties']['lon']
                longitude.append(long)
                latitude.append(lat)
            else:
                print('No results found for', i)
                # Remove the landfill sites whose coordinates are not found
                df = df.drop(index=df[df['addresses']==i].index)
                    
        else:
            print(f'Request failed with status code {response.status_code}.')
    return longitude, latitude
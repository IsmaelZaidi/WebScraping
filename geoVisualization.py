import pandas as pd
from geopy.geocoders import Nominatim
import string
import random

df = pd.read_csv('listingsCleaned.csv', sep = ';')

latitude = []
longitude = []
address = []

def randomString():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str

for i in range(361,len(df.index)-1,1):
    geolocator = Nominatim(user_agent=randomString())
    location = geolocator.geocode(df['Address'].loc[i])
    if location is not None:
        print(i)
        address.append(df['Address'].loc[i])
        latitude.append(location.latitude)
        longitude.append(location.longitude)
        dataFrame = pd.DataFrame({'Address': address, 'Latitude': latitude, 'Longitude': longitude})
        dataFrame.to_csv('geolocation.csv', index=False, encoding='utf-8')

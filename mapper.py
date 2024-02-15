import pandas as pd
import sys,time
from geopy.geocoders import Nominatim
from tqdm import tqdm
import numpy as np
import scrapper
import webbrowser

import folium
from folium.plugins import HeatMap

def Mapper(locPair):
    mapObj = folium.Map([40.428298840356405, -86.92233414617863], zoom_start = 15.2)
    HeatMap(locPair).add_to(mapObj)
    mapObj.save("output.html")

scrapper.caller()
        

df = pd.read_csv("crimeData.csv")

locationValuePairs = []

freq = df["Location"].value_counts()

for loc, frequency in freq.items():
    locationValuePairs.append((loc, frequency))

sum = 0.0

for item in locationValuePairs:
    sum += float(item[1])

print(sum)

percentSum = 0.0

# Creating a tuple with the percentage values
locPercent = []

# Setting up to get latitude and longitude
loc = Nominatim(user_agent="Geopy Library")
attach = ", West Lafayette"
max_retries = 3

counter = 0

for item in tqdm(locationValuePairs, desc="Processing", unit=" items"):
    if item[0] is None:
        continue
    percent = (item[1] / sum) * 100
    retries = 0
    while retries < max_retries:
        try:
            getLoc = loc.geocode(item[0] + attach)
            if getLoc is not None:
                locPercent.append((getLoc.latitude, getLoc.longitude, percent))
                counter += 1
            break
        except Exception as e:
            retries += 1

print("Done! \n Address Matched for " + str(counter) + " addresses out of " + str(len(locationValuePairs)))

arrLoc = np.array(locPercent)

Mapper(arrLoc)
url = "/Users/irfanfirosh/Desktop/personalProjects/CriminalMap/output.html"
webbrowser.open(url)


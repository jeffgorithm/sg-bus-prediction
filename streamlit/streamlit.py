import streamlit as st
import pandas as pd
import json

def read_location():
    coordinates = set()

    with open('bus_location.json') as f:
        for line in f.readlines():
            json_item = json.loads(line.strip('\n'))
            lat = json_item['Services'][0]['NextBus']['Latitude']
            lon = json_item['Services'][0]['NextBus']['Longitude']
            coordinates.add((float(lat), float(lon)))

    lat, lon = [], []

    for coordinate in coordinates:
        if coordinate[0] == 0:
            continue
        
        lat.append(coordinate[0])
        lon.append(coordinate[1])

    df = pd.DataFrame({
        'lat' : lat,
        'lon' : lon
    })

    return df

if __name__ == '__main__':
    df = read_location()

    st.title('Predicting Bus Travel Times')

    print(df.head())

    st.map(df)

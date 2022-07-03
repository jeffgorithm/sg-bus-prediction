import streamlit as st
import pandas as pd
import json

def read_route(file_path):
    '''Reads route file and returns list of BusStopCode and ServiceNo'''
    file = pd.read_csv(file_path, index_col=None)
    bus_stops = []

    for _, row in file.iterrows():
        bus_stops.append(str(row['BusStopCode']))

    return bus_stops

def read_bus_stops(file_path):
    bus_stop_dict = {}

    lat, lon = [], []

    with open(file_path, 'r') as f:
        for line in f.readlines():
            lines = line.strip('\n').split(',')
            lat.append(float(lines[1]))
            lon.append(float(lines[2]))
            bus_stop_dict[lines[0]] = (float(lines[1]), float(lines[2]))

    df = pd.DataFrame({
        'lat' : lat,
        'lon' : lon
    })

    return df

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
    bus_route = read_route('../data-retriever/routes/903_bus_stops.csv')
    df = read_bus_stops('903_stops_coordinates.csv')

    st.title('Predicting Bus Travel Times')

    print(df.head(30))

    st.map(df)

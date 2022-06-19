import argparse
import json
import datetime, pytz
import pandas as pd
from pandas import json_normalize
from urllib.parse import urlparse
import httplib2 as http

SLEEP_DURATION = 60

def read_route(file_path):
    '''Reads route file and returns list of BusStopCode and ServiceNo'''
    file = pd.read_csv(file_path, index_col=None)
    bus_stops = []

    for _, row in file.iterrows():
        bus_stops.append([str(row['BusStopCode']), str(row['ServiceNo'])])

    return bus_stops

def retrieve_data(handler, bus_stop_code, service_no):
    '''Performs HTTP request to server with BusStopCode and BusService'''
    try:
        target = urlparse(uri + path + 'BusStopCode=' + bus_stop_code + '&ServiceNo=' + service_no)
        response, content = handler.request(target.geturl(), 'GET', '', headers)
        json_obj = json.loads(content)
        #print(json.dumps(json_obj, indent=4))

        return json_obj
    except Exception as e:
        print(e)

def write_json(output_path, json_obj, next_stop):
    '''Adds new key to JSON object and writes to file'''
    json_obj['NextStop'] = str(next_stop)

    with open(output_path, 'a') as f:
        f.write(json.dumps(json_obj, indent=4) + '\n')

    f.close()

def write_to_file(output_file, json_obj, next_stop):
    '''A function that flattens a JSON object and writes it to a .CSV file'''
    try:
        data = json_obj['Services'][0]
        next_bus = json_normalize(data['NextBus'])
        next_bus['BusStopCode'] = bus_info[0]
        next_bus['NextBusStopCode'] = next_stop
        next_bus['ServiceNo'] = bus_info[1]
        next_bus['RetrievalTime'] = datetime.datetime.now(pytz.utc).astimezone(local_tz)
        next_bus['eta2'] = json_obj['Services'][0]['NextBus2']['EstimatedArrival']
        next_bus.to_csv(output_file, header = False, index = False)
    except Exception as e:
        print(e)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Retrieve data from LTA Datamall API')
    parser.add_argument('--key', required=True, help='API Key for accessing API')
    parser.add_argument('--route', required=True, help='Bus Service route file')
    parser.add_argument('--output', required=True, help='Output file name e.g. output.csv')
    args = parser.parse_args()

    #Initialise Authentication parameters
    headers = { 
        'AccountKey' : args.key,
        'accept' : 'application/json'
        }

    #Read Bus Service Routes Data
    bus_stops = read_route(args.route)

    #API parameters
    uri = 'http://datamall2.mytransport.sg'
    path = '/ltaodataservice/BusArrivalv2?'

    #Set timezone to local
    local_tz = pytz.timezone('Singapore')

    #Initialise http handler
    handler = http.Http()

    print("Retrieved at {}".format(str(datetime.datetime.now(pytz.utc).astimezone(local_tz))))

    for i, bus_info in enumerate(bus_stops):
        if i != len(bus_stops) - 1:
            next_stop = bus_stops[i + 1][0]
        else:
            next_stop = ''

        json_obj = retrieve_data(handler, bus_info[0], bus_info[1])

        #write_to_file(output_file, json_obj, next_stop)
        write_json(args.output, json_obj, next_stop)

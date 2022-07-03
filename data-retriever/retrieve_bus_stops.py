import argparse
import json
import requests

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Retrieve data from LTA Datamall API')
    parser.add_argument('--key', required=True, help='API Key for accessing API')
    parser.add_argument('--output', required=True, help='Output file name e.g. output.csv')
    args = parser.parse_args()

    #Initialise Authentication parameters
    headers = { 
        'AccountKey' : args.key,
        'accept' : 'application/json'
        }

    #API parameters
    api_url = 'http://datamall2.mytransport.sg/ltaodataservice/BusStops'

    #Initialise http handler
    response = requests.get(api_url, headers=headers)

    with open(args.output, 'w') as f:
        f.write(json.dumps(response.json(), indent=4))

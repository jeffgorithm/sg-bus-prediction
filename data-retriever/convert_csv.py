import json
import pandas as pd

with open('903.json', 'r') as f:
    for line in f.readlines():
        item = json.loads(line.strip('\n'))
        df = pd.json_normalize(item['Services'])
        df['BusStopCode'] = item['BusStopCode']
        df['NextStop'] = item['NextStop']
        df['CurrentTime'] = item['CurrentTime']
        print(df)
        
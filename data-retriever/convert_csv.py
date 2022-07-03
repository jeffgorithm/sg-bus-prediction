import json
import pandas as pd

with open('903.json', 'r') as f:
    for line in f.readlines():
        item = json.loads(line.strip('\n'))
        df = pd.DataFrame(index=[0])
        df['BusStopCode'] = item['BusStopCode']
        df['NextStop'] = item['NextStop']
        df['CurrentTime'] = item['CurrentTime']
        df = pd.concat([df, pd.json_normalize(item['Services'])], axis=1)
        df.to_csv('test.csv', mode='a', header=False, index=False)
        
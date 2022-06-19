import json

with open('903.json', 'r') as f:
    for line in f:
        item = json.loads(line.strip('\n'))
        print(item)


import json

json_items = []

with open('903.json') as f:
    item = ''
    for line in f.readlines():
        item += line
        if 'CurrentTime' in line:
            item += '}'
            json_items.append(item)
            item = ''

with open('903_new.json', 'w') as f:

    for i, item in enumerate(json_items):
        if i != 0:
            item = item[1:]

        json_item = json.loads(item)

        f.write(json.dumps(json_item) + '\n')
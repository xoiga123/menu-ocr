import json

with open('result.json', 'r') as file:
    js = json.load(file)

for img in js['images']:
    img['file_name'] = img['file_name'].split('/')[-1]

js['categories'] = [{
    'id': 0,
    'name': 'text'
}]

for anno in js['annotations']:
    x, y, w, h = anno['bbox']
    anno['segmentation'] = [[
        x, y, x + w, y, x + w, y + h, x, y + h
    ]]
    anno['category_id'] = 0

with open('result_fixed.json', 'w') as file:
    file.write(json.dumps(js))

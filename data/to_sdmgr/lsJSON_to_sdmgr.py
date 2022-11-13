import json
from unidecode import unidecode
import re

with open('project-3-at-2022-08-23-07-03-e72b37a0.json', 'r') as file:
    js = json.load(file)

backup_js = []
with open('train_annotation_newline.txt', 'w') as file:
    for i in js:
        running_edge = 1
        js_object = {}
        js_object['file_name'] = "images/" + i['file_upload']
        js_object['height'] = i['annotations'][0]['result'][0]['original_height']
        js_object['width'] = i['annotations'][0]['result'][0]['original_width']
        js_object['annotations'] = []
        relation_list = []
        for anno in i['annotations'][0]['result']:
            if anno['type'] == 'relation':
                relation_list.append([anno['from_id'], anno['to_id']])

        relation_dict = {}
        for index, relation in enumerate(relation_list):
            relation_dict[index] = -1

        for anno in i['annotations'][0]['result']:
            if anno['type'] == 'textarea':
                x = int(anno['value']['x'] * anno['original_width'] / 100)
                y = int(anno['value']['y'] * anno['original_height'] / 100)
                w = int(anno['value']['width'] * anno['original_width'] / 100)
                h = int(anno['value']['height'] * anno['original_height'] / 100)
                box = [x, y, x+w, y, x+w, y+h, x, y+h]
                text = unidecode(anno['value']['text'][0].replace(" ", ""))
                
                for anno2 in i['annotations'][0]['result']:
                    if anno2.get('id', False) and (anno2['id'] != anno['id']): continue
                    if anno2['type'] == 'rectanglelabels':
                        label = int(anno2['value']['rectanglelabels'][0])
                        break
                
		# this formatting is only for after training
                # format price
                # if label == 2:
                    text = text.lower()
                    text = text.replace("k", "000")
                    text = re.sub(r'[^0-9- ]', '', text)
                    text = text.strip()

                # saved edge
                if anno['id'] in sum(relation_list, []):  # flatten
                    for index, relation in enumerate(relation_list):
                        if anno['id'] in relation and relation_dict[index] == -1:
                            edge = running_edge
                            relation_dict[index] = edge
                            break
                        elif anno['id'] in relation and relation_dict[index] != -1:
                            edge = relation_dict[index]
                            break
                else:  # new edge
                    edge = running_edge
                
                running_edge += 1
                js_object['annotations'].append({
                    'box': box,
                    'text': text,
                    'label': label,
                    'edge': edge
                })
        file.write(json.dumps(js_object) + "\n")
        backup_js.append(js_object)

with open('train_annotation_backup.txt', 'w') as file:
    file.write(json.dumps(backup_js))

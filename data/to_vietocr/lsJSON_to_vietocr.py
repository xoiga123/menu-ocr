import json
import cv2

with open('project-3-at-2022-08-23-07-03-e72b37a0.json', 'r') as file:
    js = json.load(file)

count = 0
with open('train_annotation.txt', 'w') as file:
    for i in js:
        img = cv2.imread('images/'+i['file_upload'])
        for anno in i['annotations'][0]['result']:
            if anno['type'] != 'textarea': continue
            # print(anno['original_width'])
            x = int(anno['value']['x'] * anno['original_width'] / 100)
            y = int(anno['value']['y'] * anno['original_height'] / 100)
            w = int(anno['value']['width'] * anno['original_width'] / 100)
            h = int(anno['value']['height'] * anno['original_height'] / 100)
            # print(x)
            text = anno['value']['text'][0]
            crop_img = img[y:y+h, x:x+w]
            # cv2.imshow('test', crop_img)
            # cv2.waitKey(0)
            filename = f'cropped/{count:06}.jpg'
            # print(filename)
            cv2.imwrite(filename, crop_img, [cv2.IMWRITE_JPEG_QUALITY, 100])
            file.write(filename + "\t" + text + "\n")
            count += 1

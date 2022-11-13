import sys
import json
from flask import Flask, request, json
import base64
import numpy as np
import cv2
import os
import torch
torch.set_num_threads(4)
from mmocr.utils.ocr import MMOCR
from vietocr.vietocr.tool.predictor import Predictor
from vietocr.vietocr.tool.config import Cfg
from pathlib import Path

app = Flask(__name__)
vietocr_config = Cfg.load_config_from_file('vietocr/config/reg.yml')
vietocr_config['device'] = 'cpu'
vietocr_config['weights'] = 'model_weights/hub/checkpoints/reg.pth' 
# vietocr_config['weights'] = 'model_weights/hub/checkpoints/transformerocr_seq.pth' 
# vietocr_config['weights'] = 'model_weights/hub/checkpoints/transformerocr_trans.pth'   # transformer takes 20s
vietocr = Predictor(vietocr_config)

mmocr = MMOCR(
            det='DBPP_r50',
            # det='DB_r50',
            det_config='',
            # det_ckpt='model_weights/hub/checkpoints/dbnetpp_r50dcnv2_fpnc_1200e_icdar2015-20220502-d7a76fff.pth',   # replace here
            det_ckpt='model_weights/hub/checkpoints/det.pth',   # replace here
            kie='SDMGR',
            kie_config='configs/kie/sdmgr/sdmgr_novisual_60e_wildreceipt_openset.py',
            kie_ckpt='model_weights/hub/checkpoints/sdmgr_novisual_60e_wildreceipt_openset_20220803-427ec7a8.pth',   # replace here
            config_dir=os.path.join(str(Path.cwd()), 'configs/'),
            vietocr=vietocr
            )

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
    # Read data from request
    image_name = request.form.get('image_name')
    encoded_img = request.form.get('image')

    # # Convert base64 back to bytes
    img = base64.b64decode(encoded_img)
    # img = np.frombuffer(img, dtype=np.uint8)
    # img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # TODO
    # Call model for inference
    try:
        result = mmocr.readtext(img, batch_mode=True, merge=True, merge_xdist=10, details=True, image_name=image_name)
        # print(result)
        response = {
            "image_name": image_name,
            "infers": []
        }

        for pair in result:
            dct = {
                'food_name_en': 'CHICKEN STICKY RICE',   # i have no translation model
                'food_name_vi': pair[0],
                'food_price': str(pair[1])
            }
            response['infers'].append(dct)
        return json.dumps(response)
    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')

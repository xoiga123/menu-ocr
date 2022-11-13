det 7.117116212844849
stitch 0.14215826988220215
recog 6.757486343383789
kie 3.8350791931152344


det 7.283202171325684
stitch 0.14886069297790527
recog 7.208900451660156
kie 2.501375436782837

python3 mmocr/utils/ocr.py --det DBPP_r50 --det-ckpt ../khoinlg_menu/model_weights/hub/checkpoints/dbnetpp_r50dcnv2_fpnc_1200e_icdar2015-20220502-d7a76fff.pth --kie SDMGR --kie-config ../khoinlg_menu/configs/kie/sdmgr/sdmgr_novisual_60e_wildreceipt_openset.py --kie-ckpt ../khoinlg_menu/model_weights/hub/checkpoints/sdmgr_novisual_60e_wildreceipt_openset_20220803-427ec7a8.pth --batch-mode --merge --merge-xdist 10 --recog SEG 005.jpeg --output .

set_num_threads(4)
det 7  (121 imgs)
stitch 0.16561446189880371
recog 4
kie 2.5

without dconv
det 3.049887180328369
stitch 0.16561446189880371
recog 4
kie 2.5

=============================================================
labelstudio data path
/home/bao/.local/share/label-studio/media/upload

<View>
  <Image name="image" value="$ocr" zoomControl="true" rotateControl="true" zoom="true"/>
  <RectangleLabels name="label" toName="image" strokeWidth="2">
    <Label value="0" background="Aqua"/>
    <Label value="1" background="#D4380D"/>
    <Label value="2" background="#696969"/>
  </RectangleLabels>
  <Relations>
    <Relation toName="image" value="have_price"/>
  </Relations>
  <TextArea hotkey="alt+," name="transcription" toName="image" editable="true" perRegion="true" required="true" maxSubmissions="1" rows="5" strokeWidth="2"/>
</View>





TRAIN DET
export by coco in labelstudio
python3 tools/train.py configs/textdet/dbnetpp/dbnetpp_r50dcnv2_fpnc_100k_iter_synthtext.py --work-dir train_result --load-from dbnetpp_r50dcnv2_fpnc_100k_iter_synthtext-20220502-db297554.pth --gpu-id 0


1. edit category to 0
2. edit file_name
3. set segmentation same as bbox [[x1,y1...]]
https://github.com/open-mmlab/mmocr/issues/537
4 edit configs/_base_/det_datasets/toy_data.py

CUDA_VISIBLE_DEVICES=4 python3 mmocr/utils/ocr.py --det DBPP_r50 --det-ckpt train_result/epoch_20.pth --batch-mode --merge --merge-xdist 10 ../hackathon4 --output ../det_result/ --det-batch-size 8



TRAIN REG
export json-full in labelstudio
https://pbcquoc.github.io/vietocr/#dataset

1. use to_vietocr.py
2. 
python3 vietocr/train.py 


python3 vietocr/predict.py
if not (vscode-server):
    exit screen
    cat predict_result_wtf.txt
APPARENTLY, ssh + nano/vim sucks with unicode, and vscode-server is down



TRAIN KIE
export json-full in labelstudio
sdmgr expects newline delimited json LOL
https://stackoverflow.com/questions/51300674/converting-json-into-newline-delimited-json-in-python

python3 tools/train.py configs/kie/sdmgr/sdmgr_novisual_60e_wildreceipt_openset.py --work-dir train_result_kie --load-from sdmgr_novisual_60e_wildreceipt_openset_20220803-427ec7a8.pth --gpu-id 0

=============================================

RUN python cythonize.py build_ext --inplace


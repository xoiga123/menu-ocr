FROM python:3.7

WORKDIR /khoinlg_menu
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install -U openmim && \
    mim install mmcv-full && \
    pip install mmdet flask einops==0.2.0 gdown

COPY ./requirements/ /khoinlg_menu/requirements/
COPY requirements.txt /khoinlg_menu/requirements.txt
RUN pip install -r requirements.txt && \
    pip install unidecode cython

COPY . /khoinlg_menu
RUN pip install -v -e .

ENV CUDA_VISIBLE_DEVICES=-1
ENV TORCH_HOME = '/khoinlg_menu/model_weights'
CMD ["python", "./api.py"]

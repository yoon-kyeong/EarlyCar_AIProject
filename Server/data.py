# jupyter notebook에서 진행 (ipynb)
!pip install ultralytics
!pip install -e ultralytics

!pip install roboflow 
from roboflow import Roboflow
rf = Roboflow(api_key="api키") 
project = rf.workspace("project-fjp7n").project("c1-1-vwdhg")
dataset = project.version(1).download("yolov8") #데이터셋 다운 받을 때 실행할 버전 선택 필요 

%cat /home/piai/yunzzu/99_chobo/Car-detection-1/data.yaml

#전체 이미지 긁어오기 
%cd / 
from glob import glob 
img_list = glob('/home/piai/.../c1-1/train/images/*.jpg')
print(len(img_list))

import yaml
with open('/home/piai/.../c1-1/data.yaml', 'r') as f:
    data = yaml.load(f, Loader=yaml.Loader)
print(data)
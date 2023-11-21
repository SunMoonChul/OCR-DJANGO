import cv2
import torch
import os
import json
from matplotlib import pyplot as plt

from main import EasyPororoOcr

#파이토치 버전 확인, cuda device properties 확인
print('torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

# YOLOv5 detect.py 실행
os.system('python yolov5/detect.py --weights weights/best.pt --img 320 --conf 0.5 --source ./sample.jpg --project ./output --name result --save-txt')

# 결과 이미지 불러오기
img = cv2.imread('./output/result/sample.jpg')

# OpenCV에서는 이미지를 BGR로 읽기 때문에 RGB로 변환
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 이미지 출력
plt.imshow(img_rgb)
plt.show()

# txt 파일에서 바운딩 박스 정보 불러오기
with open('./output/result/labels/sample.txt') as f:
    lines = f.readlines()

# 각 객체에 대해 이미지를 잘라내고 저장
for i, line in enumerate(lines):
    # txt 파일에서는 클래스 ID와 바운딩 박스 좌표만이 저장되므로, 이를 직접 계산해야 함
    data = line.strip().split()
    class_id, center_x, center_y, width, height = map(float, data)

    # 이미지의 크기를 가져옴
    img_height, img_width = img.shape[:2]

    # 바운딩 박스의 왼쪽 위와 오른쪽 아래 좌표 계산
    top_left = ((center_x - width / 2) * img_width, (center_y - height / 2) * img_height)
    bottom_right = ((center_x + width / 2) * img_width, (center_y + height / 2) * img_height)

    # 이미지를 잘라내고 저장
    cropped = img[int(top_left[1]):int(bottom_right[1]), int(top_left[0]):int(bottom_right[0])]
    cropped_file = f'./output/result/cropped_{i}.jpg'
    cv2.imwrite(cropped_file, cropped)

    # OCR로 텍스트 추출
    ocr = EasyPororoOcr()
    text = ocr.run_ocr(cropped_file, debug=True)
    print('Result :', text)

from flask import Flask, request, jsonify
import os
import cv2
import shutil
from main import EasyPororoOcr
import time
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/uploads'

@app.route('/ocr', methods=['POST'])
def ocr_api():
    # 'yes'라는 key가 없거나, 그 값이 '1'이 아니라면 에러 메시지를 반환합니다.
    if 'yes' not in request.form or request.form['yes'] != '1':
        return jsonify({'error': 'Invalid request'}), 400

    # 'C:/uploads' 디렉토리 내의 모든 파일들을 순회합니다.
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        # 파일이 .jpg 또는 .png 확장자를 가진다면
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # yolov5 명령을 시스템에 실행시킵니다.
            os.system(
                f'python yolov5/detect.py --weights weights/best.pt --img 320 --conf 0.5 --source {file_path} --project ./output --name result --save-txt --classes 1')

            base_filename = os.path.splitext(filename)[0]

            # 인식된 라벨을 읽어옵니다.
            with open(f'./output/result/labels/{base_filename}.txt') as f:
                lines = f.readlines()

            results = []
            # 인식된 라벨이 있다면
            if len(lines) > 0:
                img = cv2.imread(file_path)
                # 각 라인에 대해
                for i, line in enumerate(lines):
                    data = line.strip().split()
                    class_id, center_x, center_y, width, height = map(float, data)
                    img_height, img_width = img.shape[:2]
                    top_left = ((center_x - width / 2) * img_width, (center_y - height / 2) * img_height)
                    bottom_right = ((center_x + width / 2) * img_width, (center_y + height / 2) * img_height)
                    cropped = img[int(top_left[1]):int(bottom_right[1]), int(top_left[0]):int(bottom_right[0])]
                    cropped_file = f'./output/result/cropped_{i}.jpg'
                    cv2.imwrite(cropped_file, cropped)

                    # OCR을 실행합니다.
                    ocr = EasyPororoOcr()
                    text = ocr.run_ocr(cropped_file, debug=True)

                    # OCR 결과가 7자리를 넘지 않거나 9자리 이상이면 오류를 반환
                    if len(text) < 7 or len(text) > 9:
                        return jsonify({'error': 'Invalid OCR result'}), 400

                    results.append(text)

                    # OCR 작업이 끝나면 외부 API에 POST 요청을 보냅니다.
                    api_url = 'http://localhost:8000/example/hello/'
                    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    data = {
                        'time': current_time,
                        'plate': results,
                    }
                    with open(file_path, 'rb') as f:
                        files = {
                            'img': f,
                        }
                        response = requests.post(api_url, data=data, files=files)

                    # 요청에 대한 응답을 확인합니다.
                    if response.status_code == 200:
                        print('성공적으로 POST 요청을 보냈습니다.')
                    else:
                        print(f'POST 요청에 실패했습니다. HTTP 상태 코드: {response.status_code}')

            # 작업이 끝난 파일과 디렉토리를 삭제합니다.
            os.remove(file_path)
            shutil.rmtree('./output/result')

    # 결과를 반환합니다.
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(port=8081, debug=True)

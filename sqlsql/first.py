# 라베파에서 받아옴
from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.\\toss'  # 파일을 저장할 경로를 지정합니다.


def create_response(message, status_code):  # 오류 메세지 등등 클라이언트로 보냄
    return message + '\n', status_code


@app.route('/imgtoss', methods=['POST'])
def imgtoss():
    # time = request.form['time']
    file = request.files['img']

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 파일 저장 디렉토리가 존재하는지 확인하고, 없다면 생성합니다.
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(filepath)

        if filename.endswith('.mp4'):
            video = cv2.VideoCapture(filepath)
            fps = video.get(cv2.CAP_PROP_FPS)  # 초당 프레임 수를 얻음

            count = 0
            while True:
                ret, frame = video.read()
                if not ret:
                    break

                if int(video.get(1)) % round(fps) == 0:  # 프레임 번호가 초당 프레임 수로 나누어 떨어지는 경우에만 이미지로 저장
                    cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], f'{filename}_{count}.jpg'), frame)
                    count += 1

            video.release()

        return create_response('성공적으로 저장되었습니다.', 200)
    except Exception as e:
        return create_response('저장 중 오류 발생: ' + str(e), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8083", debug=True)

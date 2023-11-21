# 마지막 디비 저장
import pymysql
from flask import Flask, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '.\\uploads'  # 파일을 저장할 경로를 지정합니다.


def get_db_connection():  # db 연결
    return pymysql.connect(host='127.0.0.1', port=3306, user='root',
                           passwd='qwer', db='auto', charset='utf8')


def execute_query(query, params):  # 쿼리 db로 보내기 연결
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(query, params)
        db.commit()
        return cursor.fetchall()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def create_response(message, status_code):  # 오류 메세지 등등 클라이언트로 보냄
    return message + '\n', status_code


@app.route('/uploadauto', methods=['POST'])
def uploadauto():
    time = request.form['time']
    plate = request.form['plate']
    img = request.files['img']

    filename = secure_filename(img.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # 파일 저장 디렉토리가 존재하는지 확인하고, 없다면 생성합니다.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    img.save(filepath)

    try:
        execute_query(
            "INSERT INTO violation (time, plate, imgpath) VALUES (%s, %s, %s);", (time, plate, filepath))
        return create_response('성공적으로 저장되었습니다.', 200)
    except Exception as e:
        return create_response('저장 중 오류 발생: ' + str(e), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8083", debug=True)

import os
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import pymysql
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.decorators import api_view


def get_db_connection():
    return pymysql.connect(host='localhost', port=3306, user='root',
                           passwd='qwer', db='auto', charset='utf8')


def execute_query(query, params):
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


@api_view(['POST'])
def helloAPI(request):
    upload_folder = 'C:/finaluploads'

    time = request.POST.get('time')
    plate = request.POST.get('plate')
    img = request.FILES.get('img')

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_name = default_storage.save(os.path.join(upload_folder, img.name), img)

    try:
        execute_query(
            "INSERT INTO violation (time, plate, imgpath) VALUES (%s, %s, %s);", (time, plate, file_name))
        return JsonResponse('성공적으로 저장되었습니다.', safe=False, status=200)
    except Exception as e:
        return JsonResponse('저장 중 오류 발생: ' + str(e), safe=False, status=500)

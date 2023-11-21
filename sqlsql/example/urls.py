# example 앱에 대한 url 설정
from django.urls import path, include
from .views import helloAPI

urlpatterns = [
    path("hello/", helloAPI)
]
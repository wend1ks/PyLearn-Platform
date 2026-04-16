from django.urls import path
from .views import *

app_name = "students"

urlpatterns = [
    path('', course_list, name='course_list'),
    path('<slug:slug>/', course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/',     lesson_detail, name='lesson_detail'),



]

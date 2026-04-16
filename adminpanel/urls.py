from django.urls import path,include
from .views import *

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', admin_dashboard, name='dashboard'),
    path("courses/add/", add_course, name="add_course"),
    path("courses/", course_list, name="course_list"),
    path('courses/<int:course_id>/edit/', edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', delete_course, name='delete_course'),
    path('courses/<int:course_id>/modules/add/', add_module, name='add_module'),
    path('courses/<int:course_id>/modules/', module_list, name='course_modules'),
    path('modules/<int:module_id>/edit/', edit_module, name='edit_module'),
    path('modules/<int:module_id>/delete/', delete_module, name='delete_module'),
    path('modules/<int:module_id>/lessons/add/', add_lesson, name='add_lesson'),
    path('modules/<int:module_id>/lessons/', lesson_list, name='module_lessons'),
    path('lessons/<int:lesson_id>/edit/', edit_lesson, name='edit_lesson'),
    path('lessons/<int:lesson_id>/delete/', delete_lesson, name='delete_lesson'),
    path("lessons/<int:lesson_id>/testcases/add/", add_testcase, name="add_testcase"),
    path("lessons/<int:lesson_id>/testcases/",testcase_list,name="testcase_list"),
    path('testcases/<int:testcase_id>/edit/',edit_testcase,name='edit_testcase'),
    path('testcases/<int:testcase_id>/delete/',delete_testcase,name='delete_testcase'),
]   
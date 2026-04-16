from django import forms
from courses.models import Course, Module, Lesson, TestCase

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title", "description", "slug")
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Название'}),
            'description' : forms.Textarea(attrs={'class' : 'input is-normal', 'placeholder' : 'Описание'}),
            'slug' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Строковое поле'}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']
        widgets ={
            'title' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Название'}),
            'order' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Номер модуля'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'lesson_type', 'content', 'video_url', 'order']
        widgets ={
            'title' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Название'}),
            'content' : forms.Textarea(attrs={'class' : 'input is-normal', 'placeholder' : 'Контент'}),
            'video_url' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Ссылка'}),
            'order' : forms.TextInput(attrs={'class' : 'input is-rounded', 'placeholder' : 'Номер задачи'}),
        }


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ["input_data", "expected_output",]
        widgets = {
            'input_data' : forms.Textarea(attrs={'class' : 'input is-normal', 'placeholder' : 'input_data'}),
            'expected_output' : forms.Textarea(attrs={'class' : 'input is-normal', 'placeholder' : 'expected_output'}),
        }

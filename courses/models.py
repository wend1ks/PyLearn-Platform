from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название')
    lesson_type = models.CharField(
        max_length=20,
        choices=(('text','Текст'),('video','Видео'),('task','Задача')),
        verbose_name='Тип урока',
        default='text'
    )

    content = models.TextField(blank=True, verbose_name='Описание задачи')  # описание задачи
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок выполнения')

    input_description = models.TextField(blank=True, verbose_name='Входные данные')
    output_description = models.TextField(blank=True, verbose_name='Выходные данные')
    code_template = models.TextField(blank=True, verbose_name="Шаблон кода")
    video_url = models.URLField(blank=True, null=True)


class TestCase(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='testcases', on_delete=models.CASCADE)
    input_data = models.TextField(blank=True)
    expected_output = models.TextField()
    order = models.PositiveIntegerField(default=0)


# Marker added for verification
HELLO_WORLD = "hello world"  # hello world

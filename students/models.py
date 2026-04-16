from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Lesson
from django.conf import settings


User = get_user_model()

class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='students_lessonprogress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='students_lesson_progress', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    user_image = models.ImageField(
        blank=True,
        null=True,
        help_text='Фото профиля (рекомендуемый размер 400x400)',
        upload_to='Users/user_image/'
    )
    USER_ROLES = (
        ("student", "Ученик"),
        ("admin", "Админ"),
    )
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default="student")
    phone_number = models.CharField(max_length=32)
    def is_student(self):
        return self.role == "student"

    def is_admin(self):
        return self.role == "admin"

    
    def __str__(self):
        return self.username
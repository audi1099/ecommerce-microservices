from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Добавляем новое поле 'phone'
    phone = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        blank=False,  # Поле необязательное
        verbose_name='Номер телефона'  # Человекочитаемое имя
    )

    # Дополнительные поля (по желанию):
    # profile_picture = models.ImageField(upload_to='users/')
    # birth_date = models.DateField(null=True, blank=True)

    class Meta:
        # Настраиваем название таблицы в БД
        db_table = 'auth_users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username  # Отображение в админке

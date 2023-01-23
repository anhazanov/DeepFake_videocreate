from django.db import models

class Workspace(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    owner = models.CharField(max_length=50, verbose_name='Владелец')
    path_url = models.CharField(max_length=255, unique=True, verbose_name='URL (слаг)')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


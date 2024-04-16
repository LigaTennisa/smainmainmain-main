from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


class Post(models.Model):
    COURT_CHOICES = (
        ('Court A', 'ЛИДЕР (Суходольский м-н, Восточный округ, Тюмень) '),
        ('Court B', 'Sofi-land (Лесобазовская 8а/1 Тура м-н, Ленинский округ, Тюмень) '),
    )

    GAME_CHOICES = (
        ('Новичок', 'Игра с новичком'),
        ('Профи', 'Игра с профи'),
        ('Любительская игра', 'Любительская игра'),
        ('Турнир', 'Турнир'),
    )

    title = models.CharField('Тип игры', max_length=20,
                             choices=GAME_CHOICES, default='Новичок')

    court = models.CharField('Корт', max_length=20,
                             choices=COURT_CHOICES, default='Court A')

    training_date = models.DateField(
        'Дата', default=datetime.date.today)
    training_time = models.TimeField(
        'Время', default=datetime.time(0, 0))
    preferences = models.TextField('Пожелания', default='')

    published_at = models.DateTimeField('Опубликовано', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    responders = models.ManyToManyField(User, related_name='responded_posts')

    def str(self):
        return self.title

    class Meta:
        ordering = ['-published_at']


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.author.username} to post {self.post.id}"


class Responder(models.Model):
    # Поля для класса Responder
    name = models.CharField(max_length=100)
    email = models.EmailField()
    # Другие поля и методы

    def __str__(self):
        return self.name


class ExpectedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

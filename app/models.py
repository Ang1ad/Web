"""
Definition of models.
"""
from datetime import datetime
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    
    def get_absolute_url(self):
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self):
        return self.title
    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи"

class Comment(models.Model):
    post = models.ForeignKey(Blog, null=True, blank=True, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Опубликован")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")

    class Meta:
        db_table = "Comments"
        ordering = ["-date"]
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    service = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/У'),
    ]
    
    brand = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год производства")
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES, verbose_name="Состояние")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='cars/', verbose_name="Изображение")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
        
admin.site.register(Blog) 

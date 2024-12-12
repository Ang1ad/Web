"""
Definition of models.
"""
from datetime import datetime
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

class ServiceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def clean(self):
        if self.car and self.service:
            raise ValidationError('CartItem cannot have both car and service.')
        if not self.car and not self.service:
            raise ValidationError('CartItem must have either car or service.')

    def total_price(self):
        if self.car:
            return self.quantity * self.car.price
        elif self.service:
            return self.quantity * self.service.price
        return 0
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.car and self.service:
            raise ValidationError('OrderItem cannot have both car and service.')
        if not self.car and not self.service:
            raise ValidationError('OrderItem must have either car or service.')

admin.site.register(Order)
admin.site.register(Blog) 
admin.site.register(Car)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(UserProfile)
admin.site.register(OrderItem)
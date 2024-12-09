import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import AnketaForm, AutoForm, CustomPasswordChangeForm, AvatarForm, CommentForm,  BlogForm, CustomUserCreationForm
from django.db import models
from .models import Blog, Car, CartItem, Order, UserProfile, Comment, ServiceType, Service
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import django_filters
from django_filters import rest_framework as filters

from app import forms


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/main.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Вы можете найти нас по адресу:   ',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    assert isinstance(request, HttpRequest)
    return render(
        request, 
        'app/links.html',
        {
            'title':'Ссылки',
            'message':'Ссылки на схожие ресурсы:',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день',
                '3': "Несколько раз в неделю", '4': 'Несколько раз в месяц'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[ form.cleaned_data['gender'] ]
            data['internet'] = internet[ form.cleaned_data['internet']]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = "Да"
            else:
                data['notice'] = "Нет"
                data['email'] = form.cleaned_data['email']
                data['message'] = form.cleaned_data['message']
                form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form':form,
            'data':data
        }
    )

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  
        regform = CustomUserCreationForm(request.POST)
        if regform.is_valid(): 
            reg_f = regform.save(commit=False)  
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save() 
            return redirect('home') 
    else:
        regform = CustomUserCreationForm()  
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, 
            'year': datetime.now().year,
        }
    )

def blog(request):
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }

    )

def blogpost(request, parametr):
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=post_1).order_by('-date')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user 
            comment_f.date = datetime.now() 
            comment_f.post = post_1 
            comment_f.save() 
            return redirect('blogpost', parametr=post_1.id) 
    else:
        form = CommentForm()
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, 
            'comments': comments, 
            'form': form, 
            'year': datetime.now().year,
        }
    )

def newpost(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.author = request.user  
            new_blog.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(
        request,
       'app/newpost.html',
       {
          'form': form, 
          'year': datetime.now().year,
       }
    )

def videopost(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Ролики по устройству автомобиля:',
            'year': datetime.now().year,
        }
    )
        

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year': datetime.now().year,
        }
    )

def cabinet(request):
    assert isinstance(request, HttpRequest)
    orders = Order.objects.filter(user=request.user)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(
        request,
        'app/cabinet.html',
        {
            'user': request.user,
            'orders': orders,
            'user_profile': user_profile,
            'year': datetime.now().year,
        }
    )

def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(
        request, 
        'app/change_password.html', 
        {
            'form': form,
            'year': datetime.now().year,
        }
    )

def add_avatar(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your avatar was successfully updated!')
            return redirect('add_avatar')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AvatarForm(instance=user_profile)
    return render(
        request,
       'app/add_avatar.html', 
       {
           'form': form,
           'year': datetime.now().year,
       }
    )
        
def catalog(request):
    return render(request, 'app/catalog.html', {'year': datetime.now().year,})

def car_list(request):
    brand = request.GET.get('brand', '')
    model = request.GET.get('model', '')
    year = request.GET.get('year', '')
    condition = request.GET.get('condition', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    ordering = request.GET.get('ordering', '')

    cars = Car.objects.all()

    if brand:
        cars = cars.filter(brand__icontains=brand)
    if model:
        cars = cars.filter(model__icontains=model)
    if year:
        cars = cars.filter(year=year)
    if condition:
        cars = cars.filter(condition=condition)
    if price_min:
        cars = cars.filter(price__gte=price_min)
    if price_max:
        cars = cars.filter(price__lte=price_max)

    if ordering:
        cars = cars.order_by(ordering)

    return render(request, 'app/car_list.html', {'cars': cars, 'year': datetime.now().year,})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'app/car_detail.html', {'car': car, 'year': datetime.now().year,})

def newauto(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AutoForm(request.POST, request.FILES)
        if form.is_valid():
            new_auto = form.save(commit=False)
            new_auto.author = request.user  
            new_auto.save()
            return redirect('catalog/cars')
    else:
        form = AutoForm()
    return render(
        request,
       'app/newauto.html',
       {
          'form': form, 
          'year': datetime.now().year,
       }
    )

def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
    else:
        cart_items = []
        total_price = 0
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'year': datetime.now().year})

def service_list(request):
    service_types = ServiceType.objects.all()
    return render(request, 'app/service_list.html', {'service_types': service_types, 'year': datetime.now().year,})

def service_detail(request, service_id):
    service = Service.objects.get(id=service_id)
    return render(request, 'app/service_detail.html', {'service': service, 'year': datetime.now().year,})

@login_required
def add_to_cart(request, item_type, item_id):
    if item_type == 'car':
        item = get_object_or_404(Car, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, car=item, service=None)
    elif item_type == 'service':
        item = get_object_or_404(Service, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, service=item, car=None)
    else:
        return redirect('cart')

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')
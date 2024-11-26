import re
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import AnketaForm  
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.forms import AnketaForm
from app.forms import BlogForm
from app.forms import CustomUserCreationForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
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
    return render(
        request,
        'app/cabinet.html',
        {
            'user': request.user,
            'year': datetime.now().year,
        }
    )
"""
Definition of urls for Web.
"""
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('links/', views.links, name='links'),
    path('anketa/', views.anketa, name='anketa'),
    path('registration/', views. registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'),
    path('newpost/', views.newpost, name='newpost'),
    path('videopost/', views.videopost, name='videopost'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('changepassword/', views.change_password, name='change_password'),
    path('addavatar/', views.add_avatar, name='add_avatar'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:category_id>/', views.category_detail, name='category_detail'),
    path('catalog/auto/new/', views.catalog_new_auto, name='catalog_new_auto'),
    path('catalog/auto/used/', views.catalog_used_auto, name='catalog_used_auto'),
    path('catalog/services/maintenance/', views.catalog_maintenance, name='catalog_maintenance'),
    path('catalog/services/repair/', views.catalog_repair, name='catalog_repair'),
    path('catalog/services/financing/', views.catalog_financing, name='catalog_financing'),
    path('catalog/services/insurance/', views.catalog_insurance, name='catalog_insurance'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

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
    path('catalog/cars/', views.car_list, name='car_list'),
    path('catalog/auto/<int:car_id>/', views.car_detail, name='car_detail'),
    path('newauto/', views.newauto, name='newauto'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('catalog/services/', views.service_list, name='service_list'),
    path('catalog/services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('place_order/', views.place_order, name='place_order'),
    path('newservice/', views.newservice, name='newservice'),
    path('car/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('service/<int:service_id>/edit/', views.edit_service, name='edit_service'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

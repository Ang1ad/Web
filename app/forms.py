"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Car, Comment, Service, UserProfile, Blog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
    
class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100, )
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100, )
    job = forms.CharField(label='Ваш род занятий', min_length=2, max_length=100, )
    gender = forms.ChoiceField(label='Ваш пол',
                                choices=[('1', 'Мужской'), ('2', 'Женский')],
                                widget=forms.RadioSelect, initial=1)
    internet = forms.ChoiceField(label='Вы пользуетесь интернетом',
                                choices=(('1', 'Каждый день'),
                                ('2', 'Несколько раз в день'),
                                ('3', 'Несколько раз в неделю'),
                                ('4', 'Несколько раз в месяц')), initial=1)
    notice = forms.BooleanField(label='Получать новости сайта на e-mail?',
                                required=False)
    email = forms.EmailField(label='Ваш e-mail', min_length=7)
    message = forms.CharField(label='Коротко о себе',
                                widget=forms.Textarea(attrs={'rows':12,'cols':20, 'id':'aboutYourself'}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',) 
        labels = {'text': "Комментарий"}
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
class AutoForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'year', 'condition', 'price', 'quantity', 'image')
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('service_type', 'name', 'description', 'price')
        
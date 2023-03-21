from django import forms
from .models import User, Post, Category, Comments
# from blog.models import Comments
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput,Textarea,EmailInput

# choices = [('travel', 'travel'), ('blogging','blogging'),('riding','riding')]


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'tags','featured_image','thumbnail_image')

class CommentForm(forms.ModelForm):
            class Meta:
                model = Comments
                fields = ('name','email', 'text')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'mobile_no',
                  'city', 'country', 'gender', 'username', 'password', 'image')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password',)


class EditForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
     
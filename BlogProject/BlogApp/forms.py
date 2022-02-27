from django import forms
from django.contrib.auth.models import User
from .models import Comment, Post
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class CreatePostForm(ModelForm):
    class Meta:
        model=Post
        fields = ('title', 'body', 'status', 'publish' , 'tags')

class EmailSendForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')

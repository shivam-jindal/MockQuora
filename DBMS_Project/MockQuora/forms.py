from django import forms
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('gender', 'date_of_birth', 'city', 'country', 'about_me', 'tagline', 'university', 'company', 'profile_pic', 'interests')


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class AnswerForm(forms.Form):
    answer_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 85}))
    image = forms.ImageField()


class CommentForm(forms.Form):
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 80}))


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text', 'is_anonymous', 'topic')

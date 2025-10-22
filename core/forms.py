from django import forms
from django.contrib.auth.forms import UserCreationForm


from core.models import Post, User

# from .models import Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class RegisterCandidateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

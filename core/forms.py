from django import forms
from django.contrib.auth.forms import UserCreationForm


from core.models import Post
# core/forms.py (or wherever your form is defined)
from django import forms
from .models import Post

from django.contrib.auth import get_user_model

# Get your custom User model
User = get_user_model() 


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]




class RegisterCandidateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        
    def save(self, commit=True):
        user = super().save(commit=False) 
        default_password = "1234"
        user.set_password(default_password)
        
        # 3. Save the user to the database
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

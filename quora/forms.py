from django import forms
from .models import Post
from pyuploadcare.dj.forms import ImageField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content","title")
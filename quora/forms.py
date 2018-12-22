from django import forms
from .models import Post,Answers
from pyuploadcare.dj.forms import ImageField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title","content","category",)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ("title","content",)
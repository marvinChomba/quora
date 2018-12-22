from django.contrib import admin
from .models import Post,Category,Answers,Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Answers)
admin.site.register(Profile)
from django.contrib import admin
from .models import Post,Answers,Profile

# Register your models here.
admin.site.register(Answers)
admin.site.register(Profile)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","pub_date")
    list_filter = ("pub_date","author")
    search_fields = ("title",)
    raw_id_fields = ("author",)
    filter_horizontal = ("followers",)

    #list display
    #list_filter
    #search_fields
    #raw_id_fields
    #prepoulated_fields




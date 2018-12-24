from django.contrib import admin
from .models import Post,Category,Answers,Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Answers)
admin.site.register(Profile)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title","author","category","pub_date")
    list_filter = ("pub_date","category","author")
    search_fields = ("title",)
    raw_id_fields = ("author","category")
    filter_horizontal = ("followers",)

    #list display
    #list_filter
    #search_fields
    #raw_id_fields
    #prepoulated_fields




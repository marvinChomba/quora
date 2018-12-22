from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^add/post/$",views.add_post, name="new_post"),
    url(r"^$", views.index, name = "index"),
    url(r"^follow/post/",views.follow, name = "follow")
]
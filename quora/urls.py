from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^add/post/$",views.add_post, name="new_post"),
    url(r"^$", views.index, name = "index"),
    url(r"^follow/post/",views.follow, name = "follow"),
    url(r"^post/(?P<post_id>\d+)/$", views.single_post, name = "single_post"),
    url(r"^like/comment/$",views.like_comment, name = "like_comment")
]
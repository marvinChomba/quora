from django.db import models
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import PostManager,LinkManager
from django.urls import resolve,reverse
from taggit.managers import TaggableManager
# Create your models here.
class Profile(models.Model):
    """
    This class will create a new profile for a user everytime he/she signs up
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    pic = ImageField(blank=True, manual_crop="")
    bio = models.CharField(default="Hi!", max_length=30)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    """
    This is the class that will be used to create the questions by the user
    """
    TYPE_CHOICES = (
        ("link","link"),
        ("post","post")
    )
    tags = TaggableManager()
    objects = models.Manager()
    links = LinkManager()
    posts = PostManager()
    title = models.CharField(max_length = 60)
    author = models.ForeignKey(User, related_name = "posts", null = True)
    pub_date = models.DateTimeField(auto_now_add = True)
    content = models.TextField()
    post_type = models.CharField(max_length = 10, choices = TYPE_CHOICES, default = "post")
    followers = models.ManyToManyField(User, related_name = "followers")

    def get_absolute_url(self):
        return reverse("single_post",args = [self.id])

    def __str__(self):
        return self.title
class Answers(models.Model):
    """
    This is the class that will contain the answers for the posts
    """
    author = models.ForeignKey(User,related_name = "answers")
    post = models.ForeignKey(Post, related_name = "answers")
    pub_date = models.DateTimeField(auto_now_add = True)
    title = models.CharField(max_length = 30)
    content = models.TextField()
    votes = models.ManyToManyField(User, related_name="votes")

    
    def __str__(self):
        return self.title

class Reply(models.Model):
    """
    This is the class to reply to answers
    """
    content = models.TextField()
    author = models.ForeignKey(User, related_name = "replies", on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add = True)
    answer = models.ForeignKey(Answers, related_name = "replies", on_delete = models.CASCADE)
    
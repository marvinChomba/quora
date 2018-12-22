from django.db import models
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Category(models.Model):
    """
    This is the class that will contain be used to create all the categories
    """
    name = models.CharField(max_length = 40)
    starter = models.ForeignKey(User, related_name = "categories_started",null = True)
    users_subscribed = models.ForeignKey(User, related_name = "categories_joined", null = True)

    def __str__(self):
        return self.name
class Post(models.Model):
    """
    This is the class that will be used to create the questions by the user
    """
    title = models.CharField(max_length = 60)
    author = models.ForeignKey(User, related_name = "posts", null = True)
    category = models.ForeignKey(Category, related_name = "posts", null = True)
    pub_date = models.DateTimeField(auto_now_add = True)
    content = models.TextField()
    followers = models.ManyToManyField(User, related_name = "followers")

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

from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.http import JsonResponse

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by("-pub_date")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("index")
    else:
        form = PostForm()
    for post in posts:
        if request.user in post.followers.all():
            post.user_is_following = True
        else:
            post.user_is_following = False
    context = {
        "form": form,
        "posts":posts,
    }
    return render(request,"index.html",context)

def add_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.author = request.user
            new_post.save()
            return redirect("index")
    else:
        form = PostForm()
    context = {
        "form":form
    }
    return render(request,"add_post.html",context)

def follow(request):
    post = get_object_or_404(Post, id = request.POST.get("id"))
    if request.user in post.followers.all():
        post.followers.remove(request.user)
        following = 0
    else:
        post.followers.add(request.user)
        following = 1
    data = {"following":following,"count":post.followers.all().count()}
    return JsonResponse(data)

from django.shortcuts import render,redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by("-pub_date")
    return render(request,"index.html",{"posts":posts})

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

    

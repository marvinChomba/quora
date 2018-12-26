from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm,AnswerForm
from django.contrib.auth.decorators import login_required
from .models import Post,Answers
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag
# Create your views here.
def index(request):
    objects_list = Post.objects.all().order_by("-pub_date")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect("index")
    else:
        form = PostForm()

    
    # add pagination
    paginator = Paginator(objects_list,4)

    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
        
    for post in posts:
        if request.user in post.followers.all():
            post.user_is_following = True
        else:
            post.user_is_following = False
    context = {
        "form": form,
        "posts":posts,
        "page":page
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

def tag_posts(request,tag_name):
    tag = get_object_or_404(Tag, name = tag_name)
    posts = Post.objects.filter(tags__in = [tag])
    return render(request,"tag_posts.html",{"posts":posts,"tag":tag_name})


def single_post(request,post_id):
    post = get_object_or_404(Post, id = post_id)
    answers = post.answers.all()
    
    for answer in answers:
        if request.user in answer.votes.all():
            answer.user_has_liked = True
        else:
            answer.user_has_liked = False
        print(answer.user_has_liked)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.author = request.user
            answer.post = post
            answer.save()
            return redirect("single_post", post_id = post_id)
    else:
        form = AnswerForm()
    context = {"post":post,"answers":answers,"form":form}

    return render(request, "post.html", context)

def like_comment(request):
    answer = get_object_or_404(Answers, id = request.POST.get("id"))
    if request.user in answer.votes.all():
        answer.votes.remove(request.user)
        has_liked = 0
    else:
        answer.votes.add(request.user)
        has_liked = 1

    data = {"has_liked":has_liked, "count":answer.votes.all().count()}
    return JsonResponse(data)

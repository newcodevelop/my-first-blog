from django.shortcuts import render
from django.http import HttpResponse
from .forms import PostForm
from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .models import Post

def todoView(request):
    all_posts = Post.objects.all().order_by('-created_date')
    return render(request,'todo_new.html',{'posts':all_posts})

def userView(request):
    posts_of_current_user = Post.objects.filter(author = request.user)
    return render(request, 'user_posts.html', {'posts' : posts_of_current_user})

def indexView(request):
    return render(request,'index.html')

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request,'post_detail.html',{'post':post})


def register(request):
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('todo_View')
    else:
        form = UserCreationForm()
    print('user is in reg_new {}'.format(request.user))
    return render(request, 'reg_form.html', {'form': form})





"""
def login_view(request):
    #username = request.POST['username']
    #password = request.POST['password']
    username = 'bhutum2'
    password =  'abcd$4321'
    user = authenticate(request, username=username, password=password)
    if user is not None:
        print('logged in !')
        login(request, user)
        return redirect('todo_View')
    else:
        pass
# Return an 'invalid login' error message.
"""

def logout_view(request):
    logout(request)
    return redirect('todo_View')




@login_required
def post_new(request):
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('todo_View')
    else:
        form = PostForm()
    print('user is in post_new {}'.format(request.user))
    return render(request, 'post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author = request.user)
    print(Post.objects.filter(author = request.user))
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('todo_View')
    else:
        form = PostForm(instance=post)
    print('user is in post_edit {}'.format(request.user))
    return render(request, 'post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author = request.user)
    post.delete()
    print('user is in post_delete {}'.format(request.user))
    return redirect('todo_View')
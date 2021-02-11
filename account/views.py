from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, AddPostForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required

def user_login(request):
    next = request.GET.get('next', None)
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if next:
                    return redirect(next)
                return redirect ('posts:all_posts')
            else:
                messages.error(request, 'wrong username or password', 'warning')
    else:
        form = UserLoginForm()
    return render(request, 'account/login.html', {'form':form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            login(request, user)
            messages.success(request, 'You registered successfully', 'success')
            return redirect('posts:all_posts')
    else:   
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form':form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You logged out successfully', 'success')
    return redirect('posts:all_posts')

@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id = user_id)
    posts = Post.objects.filter(user=user)
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:15])
            new_post.save()
            messages.success(request,'Tweet done', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = AddPostForm()
    return render(request, 'account/dashboard.html', {'user':user, 'posts':posts, 'form':form})
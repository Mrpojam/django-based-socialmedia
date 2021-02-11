from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import Post
# from .forms import AddPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditPostForm
from django.utils.text import slugify


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts':posts})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year = year, created__month = month, created__day = day, slug = slug)
    return render(request, 'posts/post_detail.html', {'post':post})

# def add_post(request, user_id):
#     if request.method == 'POST':
#         pass
#     else:
#         form = AddPostForm()
#     return render(request, 'posts/add_post.html', {'form':form})

@login_required
def post_delete(request, user_id, post_id):
    if user_id == request.user.id:
        Post.objects.filter(id=post_id).delete()
        messages.success(request, 'tweet deletes succussfully', 'succsess')
        return redirect('account:dashboard', user_id)
    else:
        return redirect('posts:all_posts')

@login_required
def post_edit(request, user_id, post_id):
    if request.user.id == user_id:
        post = get_object_or_404(Post, id=post_id)

        if request.method == 'POST':
            form = EditPostForm(request.POST, instance=post)
            if form.is_valid():
                ep = form.save(commit=False)
                ep.slug=slugify(form.cleaned_data['body'][:30])
                ep.save()
                messages.success(request, 'Tweet edited succussfully', 'success')
                return redirect('account:dashboard', user_id)
        else:
            form = EditPostForm(instance=post)
            return render(request, 'posts/edit_post.html', {'form':form})
    else:
        return redirect('posts:all_posts')
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import Post, Comment
# from .forms import AddPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditPostForm, AddCommentForm, AddReplyForm
from django.utils.text import slugify


def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/all_posts.html', {'posts':posts})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, created__year = year, created__month = month, created__day = day, slug = slug)
    comment = Comment.objects.filter(post=post, is_reply=False)
    reply_form = AddReplyForm()
    if request.method=='POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post 
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'your reply submitted succussfully', 'success')
    else:
        form = AddCommentForm()
    return render(request, 'posts/post_detail.html', {'post':post, 'comment':comment, 'form':form, 'reply':reply_form})

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

@login_required
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method=="POST":
        form = AddReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post 
            reply.reply = comment
            reply.is_reply=True
            reply.save()
            messages.success(request, 'reply submitted successfully', 'success')
        return redirect('posts:post_detail', post.created.year, post.created.month, post.created.day, post.slug)


from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.template.defaulttags import comment
from prompt_toolkit.validation import ValidationError

from .forms import ProfileForm, RegistrationForm, UserUpdate, ProfileUpdate, PostForm, CommentForm
from .models import Profile, Post, Comment


def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {'profile': request.user.profile})
    else:
        return render(request, 'home.html', )

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def register_view(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
    else:
        user_form = RegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'userform': user_form, 'profileform': profile_form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизировались')
            return redirect('home')
        else:
            messages.error(request, "неправильное имя пользователя или пароль")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из аккаунта')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdate(request.POST, instance=request.user)
        profile_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был обновлен')
            return redirect('profile')

    else:
        user_form = UserUpdate(instance=request.user)
        profile_form = ProfileUpdate(instance=request.user.profile)

    context = {
        'userform': user_form,
        'profileform': profile_form,
        'profile': request.user.profile
    }
    return render(request, 'profile.html', context)

@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, 'Ваш аккаунт был успешно удален')
        return redirect('home')

    return render(request, 'deleteaccount.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance = post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.user:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return redirect('post_detail', post_id=comment.post.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)

    return render(request, 'confirm_delete_comment.html', {'comment': comment})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail',  post_id = post_id)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == "POST":
        content = request.POST.get('content')
        comment = Comment.objects.create(post=post, user=request.user, content = content)
        post.comment_count += 1
        post.save()
        return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
    })

def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        return redirect('post_detail', post_id=post.id)

    if request.method == "POST":
        post.delete()
        return redirect('post_list')

    return render(request, 'confirm_delete_post.html', {'post': post})

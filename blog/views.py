
from django.shortcuts import redirect
from .models import Post, ExpectedGame
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


@login_required
def delete_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)
    context = {'post': post}

    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html', context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request,  'Форма успешно удалена.')
        return redirect('find_partner')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('find_partner')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def find_partner(request):
    posts = Post.objects.filter(author=request.user)  # Получаем посты автора
    context = {'posts': posts}
    return render(request, 'blog/find_partner.html', context)


@login_required
def edit_post(request, id):
    queryset = Post.objects.filter(author=request.user)
    post = get_object_or_404(queryset, pk=id)

    if request.method == 'GET':
        context = {'form': PostForm(instance=post), 'id': id}
        return render(request, 'blog/post_form.html', context)

    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Форма успешно обновлена.')
            return redirect('find_partner')
        else:
            messages.error(request, 'Пожалуйста, исправьте следующие ошибки:')
            return render(request, 'blog/post_form.html', {'form': form})


def home(request):

    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html')


def tournaments(request):
    return render(request, 'blog/tournaments.html')


def courts(request):
    return render(request, 'blog/courts.html')


def time(request):
    return render(request, 'blog/time.html')


def timeland(request):
    return render(request, 'blog/timeland.html')


def training(request):
    return render(request, 'blog/training.html')


def contact(request):
    return render(request, "blog/contact.html")


def aboutus(request):
    return render(request, "blog/aboutus.html")


def myrespond(request):
    return render(request, "blog/myrespond.html")


@login_required
def respond_to_post(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'POST':
        # Логика обработки отклика на пост
        # Добавляем текущего пользователя в список откликнувшихся
        post.responders.add(request.user)

        messages.success(request, 'Вы успешно откликнулись на форму.')
        return redirect('find_partner')
    else:
        return render(request, 'post_detail.html', {'post': post})


def find_partner(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "blog/find_partner.html", context)


# views.py


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # Перенаправляем
            return redirect('find_partner')
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})


def myprofile(request):
    user_posts = Post.objects.filter(author=request.user)
    context = {'user_posts': user_posts}
    return render(request, "blog/myprofile.html", context)


def accept_responder(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' and post.author == request.user:
        responder_id = request.POST.get('responder_id')
        responder = get_object_or_404(User, id=responder_id)
        post.accepted_responder = responder
        post.save()

        expected_game = ExpectedGame(user=responder)
        expected_game.save()

        messages.success(request, 'Отклик успешно принят.')
    return redirect('myprofile')


def cancel_responder(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' and post.author == request.user:
        responder_id = request.POST.get('responder_id')
        responder = get_object_or_404(User, id=responder_id)
        post.responders.remove(responder)
        post.save()

        ExpectedGame.objects.filter(user=responder).delete()

        messages.success(request, 'Отклик успешно отменен.')
    return redirect('myprofile')


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    # Здесь вы можете добавить логику для отображения профиля пользователя
    return render(request, 'blog/user_profile.html', {'user': user})


def pravila(request):
    return render(request, "blog/pravila.html")


def myposts(request):
    user_posts = Post.objects.filter(author=request.user)
    context = {'user_posts': user_posts}
    return render(request, "blog/myposts.html", context)


def responders_list(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/responders_list.html', {'post': post})


def add_to_favorites(request, post_id):
    post = Post.objects.get(id=post_id)
    user_id = request.POST.get('user_id')
    user = User.objects.get(id=user_id)

    # Добавление поста в избранное для пользователя
    user.favorites.add(post)

    # Перенаправление на страницу поиска партнера после добавления в избранное
    return redirect('find_partner')


def favorites(request):
    return render(request, "blog/favorites.html")

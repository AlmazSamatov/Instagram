from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from Instagram.forms import UserForm, RegistrationForm
from Instagram.models import Image, Like, Comment, Follow


def index(request):
    if request.user.is_authenticated:
        followings = Follow.objects.filter(follower=request.user)
        image = Image.objects.filter(user__in=followings.values('following')).order_by('-date_added')
        all_likes = Like.objects.filter(user=request.user)
        likes = []
        usernames = []
        amount_of_likes = []
        comments = []
        for img in image:
            if len(all_likes.filter(img=img)) == 1:
                likes.append(True)
            else:
                likes.append(False)
            usernames.append(img.user.username)
            amount_of_likes.append(img.amount_of_likes)
            all_comments = Comment.objects.filter(img=img)
            comm = []
            for i in all_comments:
                if i.user.username == request.user.username:
                    comm.append((i.user.username, i.comment, True))
                else:
                    comm.append((i.user.username, i.comment, False))
            comments.append(comm)
        context = {'username': request.user.username, 'image': zip(usernames, image, likes, amount_of_likes, comments)}
        return render(request, 'Instagram/index.html', context)
    else:
        form1 = UserForm()
        form2 = RegistrationForm()
        context = {'form1': form1, 'form2': form2}
        return render(request, 'Instagram/sign.html', context)

@login_required
def upload_img(request):
    if request.method == 'POST' and request.FILES.get('image') is not None:
        file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(request.user.username + '/' + file.name, file)
        img = Image.objects.create(user=request.user, path_to_img='media/' + filename)
        img.save()
    return redirect('index')


def log_in(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST['username1'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
        message = 'No such user with this username and password. Please try type again!'
        form1 = UserForm()
        form2 = RegistrationForm()
        context = {'form1': form1, 'form2': form2, 'message1': message, 'message2': ''}
        return render(request, 'Instagram/sign.html', context)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST['username2']
            password = request.POST['password_1']
            conf_password = request.POST['password_2']
            if password != conf_password:
                message = 'Passwords are different!'
                form1 = UserForm()
                form2 = RegistrationForm()
                context = {'form1': form1, 'form2': form2, 'message1': '', 'message2': message}
                return render(request, 'Instagram/register.html', context)
            if User.objects.filter(username__iexact=username).exists():
                message = 'User with this username already exists. Choose something different.'
                form1 = UserForm()
                form2 = RegistrationForm()
                context = {'form1': form1, 'form2': form2, 'message1': '', 'message2': message}
                return render(request, 'Instagram/register.html', context)
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                user1 = authenticate(request, username=username, password=password)
                if user1 is not None:
                    login(request, user1)
                    return redirect('index')
        else:
            message = 'User with this username already exists. Choose something different.'
            form1 = UserForm()
            form2 = RegistrationForm()
            context = {'form1': form1, 'form2': form2, 'message1': '', 'message2': message}
            return render(request, 'Instagram/sign.html', context)
    return redirect('index')

@login_required
def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

@login_required
def like(request):
    if request.method == 'POST':
        path = request.POST['path']
        path = path[14:]
        users_photo = path[:path.find('/')]
        liked_user = User.objects.filter(username=request.user.username)[0]
        users_photo_liked = User.objects.filter(username=users_photo)[0]
        img = Image.objects.filter(user=users_photo_liked, path_to_img='media/' + path)[0]
        like = Like.objects.filter(user=liked_user, img=img)
        is_liked = False
        if len(like) == 0:
            img.amount_of_likes = img.amount_of_likes + 1
            img.save()
            new_like = Like(user=liked_user, img=img)
            new_like.save()
        else:
            is_liked = True
            img.amount_of_likes = img.amount_of_likes - 1
            img.save()
            like[0].delete()
        return JsonResponse({"is_liked": is_liked, "amount_of_likes": img.amount_of_likes})

@login_required
def leave_comment(request):
    if request.method == 'POST':
        path = request.POST['path']
        path = path[14:]
        comment = request.POST['comment']
        users_photo = path[:path.find('/')]
        commented_user = User.objects.filter(username=request.user.username)[0]
        users_photo_commented = User.objects.filter(username=users_photo)[0]
        img = Image.objects.filter(user=users_photo_commented, path_to_img='media/' + path)[0]
        comment_obj = Comment(user=commented_user, img=img, comment=comment)
        comment_obj.save()
        return JsonResponse({'user': commented_user.username, 'comment': comment})


@login_required
def delete_comment(request):
    if request.method == 'POST':
        path = request.POST['path']
        path = path[14:]
        comment = request.POST['comment']
        users_photo = path[:path.find('/')]
        commented_user = User.objects.filter(username=request.user.username)[0]
        users_photo_commented = User.objects.filter(username=users_photo)[0]
        img = Image.objects.filter(user=users_photo_commented, path_to_img='media/' + path)[0]
        comment_obj = Comment.objects.filter(user=commented_user, img=img, comment=comment)
        if len(comment_obj) != 0:
            comment_obj.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


@login_required
def my_page(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        image = Image.objects.filter(user=user).order_by('-date_added')
        all_likes = Like.objects.filter(user=user)
        likes = []
        usernames = []
        amount_of_likes = []
        comments = []
        for img in image:
            if len(all_likes.filter(img=img)) == 1:
                likes.append(True)
            else:
                likes.append(False)
            usernames.append(img.user.username)
            amount_of_likes.append(img.amount_of_likes)
            all_comments = Comment.objects.filter(img=img)
            comm = []
            for i in all_comments:
                if request.user.username == username or i.user.username == username:
                    comm.append((i.user.username, i.comment, True))
                else:
                    comm.append((i.user.username, i.comment, False))
            comments.append(comm)
        context = {'username': request.user.username, 'image': zip(usernames, image, likes, amount_of_likes, comments)}
        return render(request, 'Instagram/my_page.html', context)
    else:
        context = {'msg': 'Пользователь с таким username не существует'}
        return render(request, 'Instagram/index.html', context)


@login_required
def search(request):
    search_request = request.GET['request']
    results = User.objects.filter(username__contains=search_request)
    followings = Follow.objects.filter(follower=request.user)
    follow = []
    for result in results:
        if result in followings:
            follow.append(True)
        else:
            follow.append(False)
    is_nothing = False
    if not results.exists():
        is_nothing = True
    context = {'results': zip(results, follow), 'is_nothing': is_nothing}
    return render(request, 'Instagram/search.html', context)
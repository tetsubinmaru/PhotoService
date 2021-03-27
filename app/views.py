from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Photo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'app/users_detail.html', {'user': user})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user, 'photos': photos})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) #Userインスタンスを作成
        if form.is_valid():
            form.save()
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            #フォームの入力値で認証できればユーザオブジェクト、できなければNoneを返す
            new_user = authenticate(
                username=input_username,
                password=input_password,
            )
        #認証成功時のみ、ユーザーをログインさせる
            if new_user is not None:
             # login関数は、認証ができなくてもログインさせることができる。（認証は上のauthenticateで実行する）
             login(request, new_user)
            return redirect('app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})
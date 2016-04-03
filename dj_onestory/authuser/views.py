from django.shortcuts import render
from django.http import HttpResponse
from .models import OneStoryUser, OneStoryUserManager
# Create your views here.
from django.contrib import auth
from .forms import UserForm, LoginForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls inde1111x.")


# Create your views here.
def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            phone = uf.cleaned_data['phone']
            date_of_birth = uf.cleaned_data['date_of_birth']
            # 将表单写入数据库
            user = OneStoryUser()
            user.email = username
            user.password = password
            user.phone = phone
            user.date_of_birth = date_of_birth
            user.save()

            # 返回注册成功页面
            return render(request, 'authuser/success.html', {'username': username})
    else:
        uf = UserForm()
    return render(request, 'authuser/register.html', {'uf': uf})


def login(request):
    if request.method == "POST":
        uf = LoginForm(request.POST)
        if uf.is_valid():
            # 获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = auth.authenticate(email=username, password=password)

            if user and user.is_authenticated():
                return render(request, 'authuser/success.html', {'username': user.nick_name})
            else:
                return HttpResponse('faiiiil')


            # 返回注册成功页面
    else:
        uf = LoginForm()
    return render(request, 'authuser/login.html', {'uf': uf})

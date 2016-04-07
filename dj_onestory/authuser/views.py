from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password

from .forms import UserForm, LoginForm
from .models import OneStoryUser, OneStoryUserManager


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
            user.password = make_password(password)
            user.phone = phone
            user.date_of_birth = date_of_birth
            # user_mange = OneStoryUserManager()
            # user_mange.create_user(email=username, date_of_birth=date_of_birth, password=password, phone=phone)
            user.save()

            # 返回注册成功页面
            return render(request, 'authuser/success.html', {'username': username})
    else:
        uf = UserForm()
    return render(request, 'authuser/register.html', {'uf': uf})


@csrf_protect
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
    else:
        uf = LoginForm()
    return render(request, 'authuser/login.html', {'uf': uf})


# login api
@csrf_exempt
def login_api(request):
    if request.method == "POST":
        post_data = request.POST
        username = post_data['username']
        password = post_data['password']
        user = auth.authenticate(email=username, password=password)
        if user and user.is_authenticated():
            # auth.login(request, user)
            pkey = user.pk
            request.session[pkey] = user.email
            print(request.session.get(pkey))
            return HttpResponse(pkey)
        else:
            return HttpResponse('faiiiil')
    else:
        return HttpResponse('faiiiil')


@csrf_exempt
def logout_api(request):
    auth.logout(request)
    return HttpResponse('ok')


@csrf_exempt
def get_login_user(request):
    print(request.session)
    if request.method == "POST":
        get_data = request.POST
        pk = get_data['pk']
        print(pk)
        return HttpResponse(request.session.get(pk))
    else:
        return HttpResponse('faiiiil')
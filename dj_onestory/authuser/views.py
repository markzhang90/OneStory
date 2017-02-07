from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password

from .forms import UserForm, LoginForm
from .models import OneStoryUser, OneStoryUserManager

import json

from core_lib.redis_manager import RedisManager
from core_lib.http_result import HttpResult
from core_lib.cypher import Cipher


def index(request):
    cypher = Cipher()
    cypher.rsa_encode('maaaaaaak   zhang  daslk')
    cypher.rsa_decode()
    # cypher.rsa_encode('tom')
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
    response = HttpResult()

    if request.method == "POST":
        post_data = request.POST

        if 'username' not in post_data or 'password' not in post_data:
            result = response.return_with_error()
            return result

        username = post_data['username']
        password = post_data['password']
        user = auth.authenticate(email=username, password=password)

        if user and user.is_authenticated():
            try:
                redis_obj = RedisManager()
            except Exception as e:
                result = response.return_with_error()
                return result
            # auth.login(request, user)
            # print(type(user))
            user_array = dict()
            user_array['pk'] = user.pk
            user_array['email'] = user.email
            user_array['phone'] = user.phone
            user_obj = json.dumps(user_array)
            response_key = redis_obj.login_update(user.pk, user_obj)
            print(response_key)
            user_array['passid'] = response_key
            del(user_array['pk'])
            if response_key:
                result = response.return_with_success(user_array)
                return result
            else:
                result = response.return_with_error()
                return result

        else:
            result = response.return_with_error()
            return result
    else:
        result = response.return_with_error()
        return result


# register api
@csrf_exempt
def register_api(request):
    response = HttpResult()

    user_dic = dict()
    if request.method == "POST":
        try:
            post_data = request.POST

            username = post_data['email']
            password = post_data['password']
            phone = post_data['phone']
            date_of_birth = post_data['date_of_birth']
            # 将表单写入数据库
            user = OneStoryUser()
            user.email = username
            user.password = make_password(password)
            user.phone = phone
            user.date_of_birth = date_of_birth
            user.save()

            redis_obj = RedisManager()

            user_array = dict()
            user_array['pk'] = user.pk
            user_array['email'] = user.email
            user_array['phone'] = user.phone
            user_obj = json.dumps(user_array)

            response_key = redis_obj.login_update(user.pk, user_obj)
            user_dic['passid'] = response_key
            user_dic['pid'] = user.pk
            result = response.return_with_success(user_dic)
            return result
        except Exception as e:
            print(e)
            result = response.return_with_error()
            return result


    result = response.return_with_error()
    return result

@csrf_exempt
def logout_api(request):
    auth.logout(request)
    return HttpResponse('ok')


@csrf_exempt
def get_login_user(request):
    response = HttpResult()

    if request.method == "POST":
        get_data = request.POST
        pk = get_data['pk']
        redis_obj = RedisManager()
        data = redis_obj.get_login(pk).decode()
        user_dic = json.loads(data)
        user_dic.pop('pk')
        if data is not None:
            result = response.return_with_success(user_dic)
            return result

    result = response.return_with_error()
    return result
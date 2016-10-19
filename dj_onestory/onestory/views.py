from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from django.conf import settings
import urllib.parse, urllib.request
import json

from .models import UserProfile, Article, Comment

from core_lib.http_result import HttpResult
from core_lib.redis_manager import RedisManager

# Create your views here.


def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")


def login_to_sys(request):
    response = HttpResult()

    data = dict()
    data['username'] = 'dog1@gamil.com'
    data['password'] = 'wc45612301'
    target_url = 'http://localhost:8000/authuser/loginapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    if req is not None:
        req_back = req.read().decode('utf-8')
        back_info = json.loads(req_back)
        if back_info['err_no'] != 0:
            result = response.return_with_error(back_info['err_no'], back_info['err_msg'])
            return result
        else:
            data = back_info['data']
            if data['passid'] is not None:
                cookie_array = dict()
                cookie_array['key'] = 'PASSID'
                cookie_array['value'] = data['passid']
                cookie_list = list()
                cookie_list.append(cookie_array)
                expire_time = settings.COOKIE_EXPIRE_TIME
                result = response.return_with_cookie(data, cookie_list, expire_time)
                return result
            else:
                result = response.return_with_error(-1, "NO PASSID")
                return result

    result = response.return_with_error(-1, "NO PASSID")
    return result


def get_log_in_user(request):

    cookie_list = request.COOKIES
    response = HttpResult()
    if 'PASSID' in cookie_list.keys():
        data = dict()
        data['pk'] = cookie_list['PASSID']
        target_url = 'http://localhost:8000/authuser/getuserapi/'
        request_para = urllib.parse.urlencode(data).encode('UTF-8')
        url = urllib.request.Request(target_url, request_para)
        req = urllib.request.urlopen(url)
        req_back = req.read().decode('utf-8')
        if req_back:
            back_info = json.loads(req_back)
            back_data = back_info['data']
            cookie_array = dict()
            cookie_array['key'] = 'PASSID'
            cookie_array['value'] = data['pk']
            cookie_list = list()
            cookie_list.append(cookie_array)
            expire_time = settings.COOKIE_EXPIRE_TIME
            result = response.return_with_cookie(back_data, cookie_list, expire_time)
            return result

    result = response.return_with_error()
    return result


def register_to_onestory(request):

    response = HttpResult()

    username = request.GET.get('username')
    pw = request.GET.get('password')
    if username is None:
        result = response.return_with_error()
        return result
    if pw is None:
        result = response.return_with_error()
        return result

    phone = '232312111'
    personal_id = '1676562'
    firstname = 'zhang'
    lastname = 'mark'
    nickname = 'oooook'
    birthddate ='1990-02-20'
    data = dict()
    data['email'] = username
    data['password'] = pw
    data['phone'] = phone
    if birthddate is None:
        birthddate = '0001-01-01'
    data['date_of_birth'] = birthddate
    target_url = 'http://localhost:8000/authuser/registerapi/'

    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    req_back = req.read().decode('utf-8')
    back_data = json.loads(req_back)
    if back_data['err_no'] == 0:
        bac_info = back_data['data']
        if bac_info['pid'] is not None and bac_info['passid'] is not None:
            try:
                new_user_profile = UserProfile()
                new_user_profile.passid = bac_info['pid']
                new_user_profile.email = username
                new_user_profile.phone = phone
                new_user_profile.nick_name = nickname
                new_user_profile.save()
            except Exception as e:
                result = response.return_with_error()
                return result

            user_bac = dict()
            user_bac['email'] = username
            user_bac['phone'] = phone

            cookie_array = dict()
            cookie_array['key'] = 'PASSID'
            cookie_array['value'] = bac_info['passid']
            cookie_list = list()
            cookie_list.append(cookie_array)
            expire_time = settings.COOKIE_EXPIRE_TIME
            result = response.return_with_cookie(user_bac, cookie_list, expire_time)
            return result

    result = response.return_with_error()
    return result


def insert_article(request):
    response = HttpResult()

    if request.method == "POST":
        post_data = request.POST
        a_title = post_data['title']
        a_content = post_data['content']
        a_ext = post_data['ext']
        a_link = post_data['link']

    a_title = "HELLO"
    a_content = "COOL"
    a_ext = "HERE"
    a_link = 'WWW.BAIDU.COM'

    cookie_list = request.COOKIES
    if 'PASSID' not in cookie_list.keys():
        result = response.return_with_error(10, 'LOGIN FIRST')
        return result

    redis_obj = RedisManager()
    data = redis_obj.get_login(cookie_list['PASSID']).decode()
    user_dic = json.loads(data)
    if not user_dic['pk']:
        result = response.return_with_error(10, 'LOGIN FIRST')
        return result

    c_user = UserProfile.objects.filter(pk=user_dic['pk'])
    if not c_user[0]:
        result = response.return_with_error(10, 'USER FAIL')
        return result

    new_article = Article()
    new_article.author = c_user[0]
    new_article.title = a_title
    new_article.content = a_content
    new_article.ext = a_ext
    new_article.link = a_link
    new_article.save()

    article = dict()
    article['aid'] = new_article.pk
    result = response.return_with_success(article)
    return result


def update_article(request):
    response = HttpResult()

    if request.method == "POST":
        post_data = request.POST
        a_id = post_data['id']
        a_title = post_data['title']
        a_content = post_data['content']
        a_ext = post_data['ext']
        a_link = post_data['link']
    a_id = 9
    a_title = "shit"
    a_content = "shit"
    a_ext = "shit"
    a_link = 'shit.BAIDU.COM'

    cookie_list = request.COOKIES
    if 'PASSID' not in cookie_list.keys():
        result = response.return_with_error(10, 'LOGIN FIRST')
        return result

    redis_obj = RedisManager()
    user_data = redis_obj.get_login(cookie_list['PASSID']).decode()
    if user_data is None:
        result = response.return_with_error(10, 'LOGIN FIRST')
        return result

    user_dic = json.loads(user_data)
    if not user_dic['pk']:
        result = response.return_with_error(10, 'LOGIN FIRST')
        return result
    c_user = UserProfile.objects.filter(pk=user_dic['pk'])
    if not c_user[0]:
        result = response.return_with_error(10, 'USER FAIL')
        return result
    res = Article.objects.filter(pk=a_id).update(
        title = a_title,
        content = a_content,
        ext = a_ext,
        link = a_link
    )
    print(res)
    if res != 1 :
        result = response.return_with_error(res)
    else:
        result = response.return_with_success(res)
    return result

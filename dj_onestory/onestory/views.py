from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
import urllib.parse, urllib.request
import json

from .models import UserProfile, Article, Comment

# Create your views here.


def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")


def login_to_sys(request):

    data = dict()
    data['username'] = 'han@gamil.com'
    data['password'] = 'wc45612301'
    target_url = 'http://localhost:8000/authuser/loginapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    req_user = req.read().decode('utf-8')
    header_content = req.getheaders()
    user_info = json.loads(req_user)
    current_user = UserProfile.objects.get(email=user_info['email'],
                                           phone=user_info['phone'])

    print(current_user.nick_name)
    # print(req.content)
    return HttpResponse(req_user)


def get_log_in_user(request):
    data = dict()
    data['pk'] = 'a6574ffa5968ebfff7f63cdf5fa6c77b'
    target_url = 'http://localhost:8000/authuser/getuserapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    return HttpResponse(req)


def register_to_onestory(request):
    username = request.GET.get('username')
    pw = request.GET.get('password')
    if username is None:
        return HttpResponse('empty username')
    if pw is None:
        return HttpResponse('empty pw')

    phone = '232312'
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
    if back_data['result'] != 'fail':
        try:
            new_user_profile = UserProfile()
            new_user_profile.passid = back_data['data']
            new_user_profile.email = username
            new_user_profile.phone = phone
            new_user_profile.nick_name = nickname
            new_user_profile.save()
        except Exception as e:
            return HttpResponse('exist user')

        return HttpResponse(new_user_profile.pk)

    else:
        return HttpResponse(back_data['data'])


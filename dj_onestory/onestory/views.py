from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
import urllib.parse, urllib.request
import json

from .models import UserProfile, Article, Comment

from core_lib.cypher import Cipher
# Create your views here.


def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")


def login_to_sys(request):

    data = dict()
    data['username'] = 'markzhang90@gmail.com'
    data['password'] = 'wc45612301'
    target_url = 'http://localhost:8000/authuser/loginapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    req_user = req.read().decode('utf-8')
    header_content = req.getheaders()
    user_info = json.loads(req_user)
    current_user = UserProfile.objects.get_or_create(passid=user_info['passid'],
                                                     email=user_info['email'],
                                                     phone=user_info['phone'])

    print(current_user)
    # print(req.content)
    return HttpResponse(req_user)


def get_log_in_user(request):
    data = dict()
    data['pk'] = '9eef56e8ac52afc4'
    target_url = 'http://localhost:8000/authuser/getuserapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    return HttpResponse(req)


def register_to_sys(
        email,
        password,
        phone,
        personal_id,
        firstname,
        lastname,
        nickname,
        birthddate):
    if email is None or password is None or phone is None:
        return False
    data = dict()
    data['email'] = email
    data['password'] = password
    data['phone'] = phone
    if birthddate is None:
        birthddate = '0001-01-01'
    data['date_of_birth'] = birthddate
    target_url = 'http://localhost:8000/authuser/registerapi/'


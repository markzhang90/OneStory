from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
import urllib.parse, urllib.request

# Create your views here.


def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")


def login_to_sys(request):

    data = dict()
    data['username'] = 'markzhang90@cat.com'
    data['password'] = 'wc45612301'
    target_url = 'http://localhost:8000/authuser/loginapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    return HttpResponse(req)


def login_to_sys2(request):
    data = dict()
    data['pk'] = '1'
    target_url = 'http://localhost:8000/authuser/getuserapi/'
    request_para = urllib.parse.urlencode(data).encode('UTF-8')
    url = urllib.request.Request(target_url, request_para)
    req = urllib.request.urlopen(url)
    return HttpResponse(req)

from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from django.conf import settings
from django.db import transaction
from ..app_settings import *
import urllib.parse
import urllib.request
import json

from ..models import UserProfile, Article, Comment

from core_lib.http_result import HttpResult
from core_lib.redis_manager import RedisManager


def index(request):
    test = dict()
    test['question_text'] = 'ccccccoooooooooooo'
    test['id'] = 10
    list = [test]
    context = {'latest_question_list': list}
    return render(request, 'onestory/login.html', context)
    # return HttpResponse("Hello, world. You're at the polls index.")


def login_to_sys(request):
    response = HttpResult()
    if request.method == 'POST':
        data = dict()
        if request.POST['username']:
            data['username'] = request.POST['username']
        if request.POST['password']:
            data['password'] = request.POST['password']
        # data['username'] = 'dog1@gamil.com'
        # data['password'] = 'wc45612301'
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
                if data['passid'] is not None and data['pk'] is not None:
                    cookie_dict = dict()
                    cookie_dict['key'] = 'PASSID'
                    cookie_dict['value'] = data['passid']
                    cookie_list = list()
                    cookie_list.append(cookie_dict)
                    expire_time = settings.COOKIE_EXPIRE_TIME
                    try:
                        c_user = UserProfile.objects.get(pk=data['pk'])
                    except UserProfile.DoesNotExist:
                        result = response.return_with_error(10, ERROR_FAIL)
                        return result
                    user_dict = dict()
                    user_dict['passid'] = data['passid']
                    user_dict['nickname'] = c_user.nick_name
                    result = response.return_with_cookie(user_dict, cookie_list, expire_time)
                    return result
                else:
                    result = response.return_with_error(-1, "NO PASSID")
                    return result

    result = response.return_with_error(-1, "NO PASSID")
    return result

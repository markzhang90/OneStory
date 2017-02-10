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


def login(request):

    context = {'header_text': 'Profile'}
    return render(request, 'onestory/login.html', context)


def index(request):

    context = {'header_text': 'Home'}
    return render(request, 'onestory/login.html', context)



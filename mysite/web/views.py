from django.shortcuts import render
from django.http import HttpResponse

from web.models import *
import hashlib
# Create your views here.


def login(request):
    """
    登入頁面顯示 跳轉首頁
    """
    if 'user' in request.COOKIES:
        return HttpResponse('checked user your cookies is' + request.COOKIES['user'])
    return render(request, "login/login.html")


def login_check(request):
    '''
    檢查使用者
    '''
    username = request.POST.get("username")
    password = request.POST.get("password").encode(encoding='utf-8')
    accounts = Account.objects.all()
    if username in accounts.username:
        password_hash256 = hashlib.sha256(password).hexdigest()
    else:
        return HttpResponse('Login failed')

    mycontext = {'A': 'B', 'hash': password_hash256}
    response = render(request, "login/login.html", mycontext)
    #response.set_cookie('user', value="username")
    return response

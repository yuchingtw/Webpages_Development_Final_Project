from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.utils import IntegrityError

from web.models import *
import hashlib
# Create your views here.

# 這是給cookies用的secret
secret = 'secret'


# login
def login(request):
    """
    登入頁面顯示 跳轉首頁 這也還沒寫完
    """
    try:
        if request.COOKIES['username'] == 'anonymous':
            pass
        accounts = Account.objects.all()
        for account in accounts:
            if hashlib.sha256((account.username + secret).encode('utf-8')).hexdigest() == request.COOKIES['username']:
                return HttpResponse('log in as ' + account.username)  # 跳轉  還沒寫
    except KeyError:
        pass

    # 沒有登入救回傳正常的登入頁面
    return render(request, "login/login.html")


def logout(request):
    """
    設定 cookeis username 為 anonymous
    """
    try:
        response = HttpResponse('log out success')
        response.set_cookie('username', value="anonymous")
        return response  # 跳轉  還沒寫
    except KeyError:
        pass


def login_check(request):
    '''
    檢查使用者 確認正確使用者
    '''
    username = request.POST.get("username")
    password_sha256 = hashlib.sha256(request.POST.get(
        "password").encode(encoding='utf-8')).hexdigest()
    account = get_object_or_404(Account, username=username)
    if account.password_sha256 == password_sha256:
        response = HttpResponse("login success as " + username)
        response.set_cookie('username', value=hashlib.sha256((
            username + secret).encode('utf-8')).hexdigest())
        return response
    return HttpResponse('LOGIN FAILD')


def register(request):
    '''
    密碼還沒做hash設定
    '''

    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            password_sha256 = hashlib.sha256(request.POST.get(
                "password").encode(encoding='utf-8')).hexdigest()
            password_sha256_repeat = hashlib.sha256(request.POST.get(
                "password_repeat").encode(encoding='utf-8')).hexdigest()
            name = request.POST.get("name")

            if password_sha256 != password_sha256_repeat:
                raise Exception("密碼前後不一致")
            if username == '' or password_sha256 == '' or name == '':
                raise Exception("輸入空白值")
            Account.objects.create(
                username=username, password_sha256=password_sha256, name=name)
        except IntegrityError:
            return HttpResponse('存在相同用戶名')
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('註冊成功')

    return render(request, 'register/register.html')

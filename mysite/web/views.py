from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from web.models import Account
# Create your views here.

HOME_PAGE = 'index.html'
LOGIN_PAGE = 'login/login.html'
REGISTER_PAGE = 'register/register.html'
LOGIN_REQUIRED_PAGE = 'logrequirePage.html'


def index(request):
    return render(request, HOME_PAGE)


def login(request):
    """
    登入頁面顯示 跳轉首頁 這也還沒寫完
    """
    if request.user.username == "AnonymousUser":
        return render(request, HOME_PAGE)
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
        else:
            return render(request, LOGIN_PAGE)
    else:
        return render(request, LOGIN_PAGE)
    return render(request, HOME_PAGE)


@login_required
def login_require_page(request):
    """
    測試登入權限
    """
    return render(request, LOGIN_REQUIRED_PAGE)


def logout(request):
    """
    設定 cookeis username 為 anonymous
    """
    auth.logout(request)
    return render(request, HOME_PAGE)


def register(request):
    '''
    註冊
    '''
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            password_repeat = request.POST.get("password_repeat")
            nickname = request.POST.get("nickname")
            email = request.POST.get("email")
            if password != password_repeat:
                raise Exception("密碼前後不一致")
            if username == '' or password == '' or nickname == '':
                raise Exception("輸入空白值")
            account = Account.objects._create_user(
                username, email, password, nickname=nickname)

        except IntegrityError:
            return HttpResponse('存在相同用戶名')
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success as ' + account.username)

    return render(request, REGISTER_PAGE)

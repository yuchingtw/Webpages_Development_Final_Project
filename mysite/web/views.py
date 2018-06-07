from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from web.utils import check_code
from io import BytesIO
<<<<<<< HEAD
from web.models import Account
import os,shutil


=======

from web.models import Account, Video
>>>>>>> 873451fdfe00eabd416b3f83e9cc4267fadcd75b
# Create your views here.
HOME_PAGE = 'index.html'
HOME_PAGE_URL = "/web/index/"
LOGIN_PAGE = 'login/login.html'
LOGIN_PAGE_URL = "/web/login/"
REGISTER_PAGE = 'register/register.html'
LOGIN_REQUIRED_PAGE = 'logrequirePage.html'
UPLOAD_PAGE = 'videoupload.html'


def index(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    return render(request, HOME_PAGE, context)


def login(request):
    """
    登入頁面顯示 跳轉首頁 這也還沒寫完
    """
    if str(request.user) != "AnonymousUser":
        return HttpResponseRedirect(HOME_PAGE_URL)
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)

            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponseRedirect(HOME_PAGE_URL)
        else:
            return render(request, LOGIN_PAGE)
    else:
        context = dict()
        if request.GET.get('next'):
            context = {'next': request.GET.get('next')}
        return render(request, LOGIN_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def login_require_page(request):
    """
    測試登入權限
    """
    return render(request, LOGIN_REQUIRED_PAGE)


def logout(request):
    """
    內建方法登出
    """
    auth.logout(request)
    return HttpResponseRedirect('/web/index')


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
            code = request.POST.get('code', '')
            if code != request.session.get('check_code', 'error'):
                raise Exception("驗證碼輸入錯誤")
            account = Account.objects._create_user(
                username, email, password, nickname=nickname)

        except IntegrityError:
            return HttpResponse('存在相同用戶名')
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('success as ' + account.username)

    return render(request, REGISTER_PAGE)


def create_code_img(request):
    # 在記憶體中空出位置，存放產生的圖片
    f = BytesIO()
    img, code = check_code.create_code()
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


@login_required(login_url=LOGIN_PAGE_URL)
def upload_video(request):
    if request.method == 'POST':
        user = get_object_or_404(Account, username=request.user)
        up_video = Video()
        up_video.title = request.POST.get("title")
        up_video.photo = request.FILES["image"]
        up_video.video_path = request.FILES["videofile"]
        up_video.content = request.POST.get("description")
        up_video.classify = request.POST.get("tag")
        up_video.vidoe_length = 0
        up_video.save()

    return render(request, UPLOAD_PAGE)

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from web.utils import check_code
from io import BytesIO
from web.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.request import urlopen
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
HOME_PAGE = 'index.html'
HOME_PAGE_URL = "/web/index/"
LOGIN_PAGE = 'login/login.html'
LOGIN_PAGE_URL = "/web/login/"
REGISTER_PAGE = 'register/register.html'
LOGIN_REQUIRED_PAGE = 'logrequirePage.html'
UPLOAD_PAGE = 'videoupload.html'
POST_SHOW_PAGE = 'post/post_show.html'
POST_LIST_PAGE = 'post/post_list.html'
VIDEO_SHOW_PAGE = 'video/video_show.html'
VIDEO_LIST_PAGE = 'video/video_list.html'

# CoinHive
COINHIVE_ENABLE = '0'
COINHIVE_BALANCE_URL = 'https://api.coinhive.com/user/balance'
COINHIVE_SECRET = 'h3YhLOhht6CZN7uqR0GD6BRuin6gEjtM'


def index(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    urlrequset = urlopen(COINHIVE_BALANCE_URL + "?secret=" +
                         COINHIVE_SECRET + "&name=" + str(request.user))
    context.update(json.loads(urlrequset.read()))
    context['COINHIVE_ENABLE'] = COINHIVE_ENABLE
    return render(request, HOME_PAGE, context)


def login(request):
    """
    登入頁面顯示 跳轉首頁 這也還沒寫完
    """
    print(request.POST)
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


@csrf_exempt
def verify_username(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get("username")
        # QuerySet is null
        if(Account.objects.filter(username=username).count() == 0):
            response = "null"
        else:
            response = "exist"

    return HttpResponse(json.dumps(response), content_type="application/json")


"""
    return HttpResponse(
        json.dumps(),
        content_type='application/json')
"""

"""
驗證碼產生
"""


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
        up_video.video_length = 0
        up_video.save()

    return render(request, UPLOAD_PAGE)


"""
文章列表+顯示
"""


def post_show(request):
    upid = request.GET.get('q')
    post = Post.objects.get(upid=upid)
    return render(request, POST_SHOW_PAGE, {'post': post})


def post_list(request):
    post = Post.objects.all()
    current_page = request.GET.get('p')
    paginator = Paginator(post, 10)  # 每頁顯示10筆
    try:
        page = paginator.page(current_page)  # 根據current_page顯示頁數
    except EmptyPage as e:
        page = paginator.page(1)  # 如果get到了沒有的頁數則顯示第一頁
    except PageNotAnInteger as e:
        page = paginator.page(1)  # 傳入非數字也顯示第一頁

    return render(request, POST_LIST_PAGE, {'page': page})


"""
影片列表+顯示
"""


def video_show(request):
    uvid = request.GET.get('q')
    video = Video.objects.get(uvid=uvid)
    return render(request, VIDEO_SHOW_PAGE, {'video': video})


def video_list(request):
    video = Video.objects.all()
    current_page = request.GET.get('p')
    paginator = Paginator(video, 10)  # 每頁顯示10筆
    try:
        page = paginator.page(current_page)  # 根據current_page顯示頁數
    except EmptyPage as e:
        page = paginator.page(1)  # 如果get到了沒有的頁數則顯示第一頁
    except PageNotAnInteger as e:
        page = paginator.page(1)  # 傳入非數字也顯示第一頁

    return render(request, VIDEO_LIST_PAGE, {'page': page})

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
import requests as wtf
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.serializers import serialize

# Create your views here.
HOME_PAGE = 'index.html'
HOME_PAGE_URL = "/index/"
LOGIN_PAGE = 'login/login.html'
LOGIN_PAGE_URL = "/login/"
REGISTER_PAGE = 'register/register.html'
LOGIN_REQUIRED_PAGE = 'logrequirePage.html'
VIDEO_NEW_PAGE = 'video/video_new.html'
VIDEO_SHOW_PAGE = 'video/video_show.html'
VIDEO_LIST_PAGE = 'video/video_list.html'
VIDEO_EDIT_PAGE = 'video/video_edit.html'
POST_SHOW_PAGE = 'post/post_show.html'
POST_SHOW_URL = '/postShow/?'
POST_EDIT_URL = '/postedit/?'
POST_DEL_URL = '/postdel/?'
POST_EDIT_PAGE = 'post/post_edit.html'
POST_LIST_PAGE = 'post/post_list.html'
POST_NEW_PAGE = 'post/post_new.html'
DASHBOARD_PAGE = 'dashboard/dashboard.html'
DASHBOARD_COIN_PAGE = 'dashboard/dashboard_coin.html'
DASHBOARD_POSTS_PAGE = 'dashboard/dashboard_posts.html'
DASHBOARD_PROFILE_PAGE = 'dashboard/dashboard_profile.html'
DASHBOARD_VIDEOS_PAGE = 'dashboard/dashboard_videos.html'
DASHBOARD_URL = '/dashboard'
DASHBOARD_POSTSMANAGE_PAGE = 'dashboard/manage.html'
SEARCH_RESULT_PAGE = 'searchresult.html'
SELF_INTRO_PAGE = 'self_intro.html'


# CoinHive
COINHIVE_ENABLE = '0'
COINHIVE_BALANCE_URL = 'https://api.coinhive.com/user/balance'
COINHIVE_WITHDRAW_URL = 'https://api.coinhive.com/user/withdraw'
COINHIVE_SECRET = 'h3YhLOhht6CZN7uqR0GD6BRuin6gEjtM'


def index(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    post = Post.objects.order_by('-publish_time')[:6]
    video = Video.objects.order_by('-publish_time')[:6]
    post_pop = Post.objects.order_by('-like')[:6]
    video_pop = Video.objects.order_by('-like')[:6]
    context.update({'post': post, 'video': video,
                    'post_pop': post_pop, 'video_pop': video_pop})

    context['COINHIVE_ENABLE'] = COINHIVE_ENABLE

    if str(request.user) == 'admin':
        context.update({'admin': True})

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
    return HttpResponseRedirect('/index/')


def register(request):
    '''
    註冊
    '''
    context = dict()
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
            context = {"alert": '「{0}」註冊成功！'.format(
                account.username), "result": "ok"}

        except IntegrityError:
            context = {"alert": "存在相同用戶名", "result": "no"}
            return render(request, REGISTER_PAGE, context)
        except Exception as e:
            context = {"alert": str(e), "result": "no"}
            return render(request, REGISTER_PAGE, context)
        return render(request, REGISTER_PAGE, context)
    context = {"alert": "", "result": "nothing"}
    return render(request, REGISTER_PAGE, context)


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

    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")


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
def video_new(request):

    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    if request.method == 'POST':
        user = get_object_or_404(Account, username=request.user)
        up_video = Video()
        up_video.title = request.POST.get("title")
        up_video.photo = request.FILES["image"]
        up_video.video_path = request.FILES["videofile"]
        up_video.content = request.POST.get("description")
        up_video.classify = request.POST.get("tag")
        up_video.video_length = 0
        up_video.uploder = user
        up_video.save()
        return HttpResponseRedirect('/web/index')

    return render(request, VIDEO_NEW_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def new_post(request):

    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    if request.method == 'POST':
        user = get_object_or_404(Account, username=request.user)
        new_post = Post()
        new_post.title = request.POST.get("title")
        new_post.photo = request.FILES["image"]
        new_post.content = request.POST.get("content")
        new_post.classify = request.POST.get("tag")
        new_post.click_times = 0
        new_post.watched_time = 0
        new_post.like = 0
        new_post.dislike = 0
        new_post.uploder = user
        new_post.save()
        return HttpResponseRedirect('/web/index')

    return render(request, POST_NEW_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def dashboard(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    user = Account.objects.get(username=request.user)
    posts_set = Post.objects.filter(
        uploder__exact=user).order_by('-publish_time')[:6]
    videos_set = Video.objects.filter(
        uploder__exact=user).order_by('-publish_time')[:6]
    context["user"] = user
    context["videos"] = videos_set
    context["posts"] = posts_set

    return render(request, DASHBOARD_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def dashboard_profile(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    user = Account.objects.get(username=request.user)
    if request.method == 'POST':
        user.nickname = request.POST.get("nickname")
        user.intro = request.POST.get('intro')
        user.email = request.POST.get('email')
        user.xmr_address = request.POST.get('xmr_address')
        user.save()
    context.update({'user': user})
    return render(request, DASHBOARD_PROFILE_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def dashboard_posts(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    user = Account.objects.get(username=request.user)
    posts_set = Post.objects.filter(uploder__exact=user)
    context.update({"posts": posts_set})
    return render(request, DASHBOARD_POSTS_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def dashboard_videos(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    user = Account.objects.get(username=request.user)
    videos_set = Video.objects.filter(uploder__exact=user)
    context.update({"videos": videos_set})
    return render(request, DASHBOARD_VIDEOS_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def dashboard_coin(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    return render(request, DASHBOARD_COIN_PAGE, context)


"""
文章顯示、列表、編輯、刪除
"""


def post_show(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    upid = request.GET.get('q')
    post = Post.objects.get(upid=upid)
    uploder = Account.objects.get(username=post.uploder)
    print(uploder)
    context['post'] = post
    context['uploder'] = uploder
    return render(request, POST_SHOW_PAGE, context)


def post_list(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    post = Post.objects.all()
    current_page = request.GET.get('p')
    paginator = Paginator(post, 5)  # 每頁顯示5筆
    try:
        page = paginator.page(current_page)  # 根據current_page顯示頁數
    except EmptyPage as e:
        page = paginator.page(1)  # 如果get到了沒有的頁數則顯示第一頁
    except PageNotAnInteger as e:
        page = paginator.page(1)  # 傳入非數字也顯示第一頁
    context['page'] = page
    return render(request, POST_LIST_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def post_edit(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    pid = request.GET.get("q")
    post = Post.objects.get(upid__exact=pid)
    if post.uploder != request.user:
        return render(request, HOME_PAGE)
    if request.method == 'POST':
        post.title = request.POST.get("title")
        try:
            post.photo = request.FILES["image"]
        except Exception:
            pass
        post.content = request.POST.get("content")
        post.classify = request.POST.get("tag")
        post.save()
        return HttpResponseRedirect(DASHBOARD_URL)

    context['post'] = post
    return render(request, POST_EDIT_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def post_del(request):
    pid = request.GET.get("q")
    post = Post.objects.get(upid__exact=pid)
    print(post)
    post.delete()
    return HttpResponseRedirect(DASHBOARD_URL)


"""
影片顯示、列表、編輯、刪除
"""


def video_show(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    uvid = request.GET.get('q')
    video = Video.objects.get(uvid=uvid)
    uploder = Account.objects.get(username=video.uploder)
    print(uploder)
    context['video'] = video
    context['uploder'] = uploder
    return render(request, VIDEO_SHOW_PAGE, context)


def video_list(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    video = Video.objects.all()
    current_page = request.GET.get('p')
    paginator = Paginator(video, 5)  # 每頁顯示5筆
    try:
        page = paginator.page(current_page)  # 根據current_page顯示頁數
    except EmptyPage as e:
        page = paginator.page(1)  # 如果get到了沒有的頁數則顯示第一頁
    except PageNotAnInteger as e:
        page = paginator.page(1)  # 傳入非數字也顯示第一頁
    context['page'] = page
    return render(request, VIDEO_LIST_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def video_edit(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    uvid = request.GET.get("q")
    video = Video.objects.get(uvid__exact=uvid)
    if video.uploder != request.user:
        return render(request, HOME_PAGE)
    if request.method == 'POST':
        video.title = request.POST.get("title")
        try:
            video.photo = request.FILES["image"]
        except Exception:
            pass
        try:
            video_path = request.FILES["videofile"]
        except Exception:
            pass

        video.content = request.POST.get("description")
        video.classify = request.POST.get("tag")
        video.save()
        return HttpResponseRedirect(DASHBOARD_URL)

    context['video'] = video
    return render(request, VIDEO_EDIT_PAGE, context)


@login_required(login_url=LOGIN_PAGE_URL)
def video_del(request):
    vid = request.GET.get("q")
    video = Video.objects.get(uvid__exact=vid)
    video.delete()
    print(video)
    return HttpResponseRedirect(DASHBOARD_URL)


def search(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}
    query = request.POST.get("need")
    videos_set = Video.objects.filter(
        Q(title__contains=query) | Q(classify__contains=query))
    posts_set = Post.objects.filter(
        Q(title__contains=query) | Q(classify__contains=query) | Q(content__contains=query))
    print(videos_set)
    content = {'videos': videos_set, 'posts': posts_set,
               'POST_SHOW_URL': POST_SHOW_URL}
    content.update(context)
    return render(request, SEARCH_RESULT_PAGE, content)


def selfintro(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    username = request.GET.get('q')
    user = Account.objects.get(username=username)
    videos_set = Video.objects.filter(uploder__exact=user)
    posts_set = Post.objects.filter(uploder__exact=user)
    context["user"] = user
    context["videos"] = videos_set
    context["posts"] = posts_set
    return render(request, SELF_INTRO_PAGE, context)


@csrf_exempt
def get_videos_set(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get("username")
    user = Account.objects.get(username=username)
    videos_set = Video.objects.filter(uploder__exact=user)
    report = serialize('json', videos_set)
    return HttpResponse(report, content_type="application/json")


@csrf_exempt
def get_posts_set(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get("username")
    user = Account.objects.get(username=username)
    posts_set = Post.objects.filter(uploder__exact=user)
    report = serialize('json', posts_set)
    return HttpResponse(report, content_type="application/json")


@csrf_exempt
def set_video_watchedtime(request):
    data = json.loads(request.body.decode('utf-8'))
    time = data.get("time")
    uvid = data.get("uvid")
    video = Video.objects.get(uvid=uvid)
    video.watched_time = video.watched_time + time
    video.save()
    return HttpResponse("", content_type="application/json")


@csrf_exempt
def set_post_watchedtime(request):
    data = json.loads(request.body.decode('utf-8'))
    time = data.get("time")
    upid = data.get("upid")
    post = Post.objects.get(upid=upid)
    post.watched_time = post.watched_time + time
    post.save()
    return HttpResponse("", content_type="application/json")


@csrf_exempt
def calculate(request):
    all_watched_time = 0
    withdraw_hash = 0
    videos_set = Video.objects.all()
    posts_set = Post.objects.all()
    for video in videos_set:
        all_watched_time = all_watched_time + video.watched_time
    for post in posts_set:
        all_watched_time = all_watched_time + post.watched_time
    urlrequset = urlopen(COINHIVE_BALANCE_URL + "?secret=" +
                         COINHIVE_SECRET + "&name=" + "admin")
    coinhive_result = json.loads(urlrequset.read())
    persecon_get_coin = int(coinhive_result['balance'] / all_watched_time)
    withdraw_hash_assert = persecon_get_coin * all_watched_time
    print(withdraw_hash_assert)

    for video in videos_set:
        if video.watched_time > 0:
            user = Account.objects.get(username=video.uploder)
            user.gold_coin += video.watched_time * persecon_get_coin
            withdraw_hash += video.watched_time * persecon_get_coin
            video.watched_time = 0
            video.save()
            user.save()
    for post in posts_set:
        if post.watched_time > 0:
            user = Account.objects.get(username=post.uploder)
            user.gold_coin += post.watched_time * persecon_get_coin
            withdraw_hash += post.watched_time * persecon_get_coin
            post.watched_time = 0
            post.save()
            user.save()
    print(withdraw_hash)
    data = {
        'secret': COINHIVE_SECRET,
        'name': 'admin',
        'amount': withdraw_hash
    }
    print(data)
    response = wtf.post(COINHIVE_WITHDRAW_URL, data)
    print(response)
    pass

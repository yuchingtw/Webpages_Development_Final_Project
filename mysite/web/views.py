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
from django.db.models import Q
from django.core.serializers import serialize

# Create your views here.
HOME_PAGE = 'index.html'
HOME_PAGE_URL = "/web/index/"
LOGIN_PAGE = 'login/login.html'
LOGIN_PAGE_URL = "/web/login/"
REGISTER_PAGE = 'register/register.html'
LOGIN_REQUIRED_PAGE = 'logrequirePage.html'
VIDEO_NEW_PAGE = 'video/video_new.html'
POST_SHOW_PAGE = 'post/post_show.html'
POST_SHOW_URL = '/postShow/?'
POST_EDIT_URL = '/postedit/?'
POST_DEL_URL = '/postdel/?'
POST_EDIT_PAGE = 'post/post_edit.html'
POST_LIST_PAGE = 'post/post_list.html'
POST_NEW_PAGE = 'post/post_new.html'
VIDEO_SHOW_PAGE = 'video/video_show.html'
VIDEO_LIST_PAGE = 'video/video_list.html'
DASHBOARD_PAGE = 'dashboard/dashboard.html'
DASHBOARD_URL = '/dashboard'
DASHBOARD_POSTSMANAGE_PAGE = 'dashboard/manage.html'
SEARCH_RESULT_PAGE = 'searchresult.html'
SELF_INTRO_PAGE = 'self_intro.html'


# CoinHive
COINHIVE_ENABLE = '0'
COINHIVE_BALANCE_URL = 'https://api.coinhive.com/user/balance'
COINHIVE_SECRET = 'h3YhLOhht6CZN7uqR0GD6BRuin6gEjtM'


def index(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    post = Post.objects.order_by('-publish_time')[:6]
    video = Video.objects.order_by('-publish_time')[:6]
    post_pop = Post.objects.order_by('-like')[:6]
    video_pop = Video.objects.order_by('-like')[:6]
    print(post)
    context.update({'post': post, 'video': video,
                    'post_pop': post_pop, 'video_pop': video_pop})

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
def post_edit(request):
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
    return render(request, POST_EDIT_PAGE, {'post': post})


@login_required(login_url=LOGIN_PAGE_URL)
def post_del(request):
    pid = request.GET.get("q")
    post = Post.objects.get(upid__exact=pid)
    print(post)
    post.delete()
    return HttpResponseRedirect(DASHBOARD_URL)


@login_required(login_url=LOGIN_PAGE_URL)
def dashboard(request):
    user = Account.objects.get(username=request.user)
    posts_set = Post.objects.filter(uploder__exact=user)
    videos_set = Video.objects.filter(uploder__exact=user)
    return render(request, DASHBOARD_PAGE, {'user': user, 'posts': posts_set, "videos": videos_set})


"""
文章列表+顯示
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


def video_edit(request):
    pass


def video_del(request):
    pass


def search(request):
    query = request.POST.get("need")
    videos_set = Video.objects.filter(
        Q(title__contains=query) | Q(classify__contains=query))
    posts_set = Post.objects.filter(
        Q(title__contains=query) | Q(classify__contains=query) | Q(content__contains=query))
    print(videos_set)
    content = {'videos': videos_set, 'posts': posts_set,
               'POST_SHOW_URL': POST_SHOW_URL}
    return render(request, SEARCH_RESULT_PAGE, content)


def selfintro(request):
    context = dict()
    if str(request.user) != "AnonymousUser":
        context = {'anon': 'true'}

    username = request.GET.get('q')
    user = Account.objects.get(username=username)
    videos_set = Video.objects.filter(uploder__exact=user)
    posts_set = Post.objects.filter(uploder__exact=user)

    return render(request, SELF_INTRO_PAGE, {"user": user, "videos": videos_set, "posts": posts_set})


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
    report = ""
    return HttpResponse(report, content_type="application/json")

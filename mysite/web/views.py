from django.shortcuts import render
from django.http import HttpResponse

from web.models import *
import hashlib
# Create your views here.


#login
def login(request):
    """
    登入頁面顯示 跳轉首頁 這也還沒寫完
    """
    if 'user' in request.COOKIES:
        return HttpResponse('checked user your cookies is' + request.COOKIES['user'])
    return render(request, "login/login.html")


def login_check(request):
    '''
    檢查使用者 還沒寫完拉
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
    #response.set_cookie(hash('user'+'secret'), value="username")
    return response

#rigister
def register(request):
    '''
    密碼還沒做hash設定
    '''
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password").encode(encoding='utf-8')
        name=request.POST.get("name")
        if(username==''or password=='' or name==''  ):
            return HttpResponse('欄位不能為空白')
        Account.objects.create(username=username,password_sha256=password,name=name)
        return HttpResponse('註冊成功')
        
    return render(request,'register/register.html')

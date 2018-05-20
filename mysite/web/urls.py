from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'login/', views.login, name="login_page"),
    url(r'register/', views.register, name="register_page"),
    url(r'login_check/', views.login_check, name='login_check'),
]

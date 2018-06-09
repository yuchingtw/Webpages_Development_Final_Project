from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'login/', views.login, name="login_page"),
    url(r'logout/', views.logout, name="logout"),
    url(r'register/', views.register, name="register_page"),
    url(r'logrequired/', views.login_require_page, name="logrequired"),
    url(r'index/', views.index, name="index"),
    url(r'create_code/', views.create_code_img, name="create_code"),
    url(r'uploadvideo/', views.upload_video),
    url(r'postShow/', views.post_show, name="post_show"),
    url(r'postList/', views.post_list, name="post_list"),
    url(r'videoShow/', views.video_show, name="video_show"),
    url(r'videoList/', views.video_list, name="video_list"),
    url(r'verify_username/?', views.verify_username, name="verify_username"),
]

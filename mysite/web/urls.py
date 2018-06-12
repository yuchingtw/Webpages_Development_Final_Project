from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'index/', views.index, name="index"),
    url(r'login/', views.login, name="login_page"),
    url(r'register/', views.register, name="register_page"),
    url(r'search_result/', views.search, name="search"),
    url(r'selfintro/', views.selfintro, name="selfintro"),

    url(r'dashboard/profile', views.dashboard_profile, name="dashboard_profile"),
    url(r'dashboard/posts', views.dashboard_posts, name="dashboard_posts"),
    url(r'dashboard/videos', views.dashboard_videos, name="dashboard_videos"),
    url(r'dashboard/coin', views.dashboard_coin, name="dashboard_coin"),
    url(r'dashboard/', views.dashboard, name="dashboard"),

    url(r'postShow/', views.post_show, name="post_show"),
    url(r'postList/', views.post_list, name="post_list"),
    url(r'postnew/', views.new_post, name="new_post"),
    url(r'postedit/', views.post_edit, name="post_edit"),
    url(r'postdel/', views.post_del, name="post_del"),
    url(r'video_del/', views.video_del, name="video_del"),
    url(r'video_edit/', views.video_edit, name="video_edit"),
    url(r'video_new/', views.video_new, name="video_new"),
    url(r'videoShow/', views.video_show, name="video_show"),
    url(r'videoList/', views.video_list, name="video_list"),

    url(r'verify_username/?', views.verify_username, name="verify_username"),
    url(r'logout/', views.logout, name="logout"),
    url(r'create_code/', views.create_code_img, name="create_code"),
    url(r'get_videos_set/', views.get_videos_set, name="get_videos_set"),
    url(r'get_posts_set/', views.get_posts_set, name="get_posts_set"),
    url(r'set_video_watchedtime/', views.set_video_watchedtime,
        name="set_video_watchedtime"),
    url(r'set_post_watchedtime/', views.set_post_watchedtime,
        name="set_post_watchedtime"),
    url(r'calculate/', views.calculate, name="calculate")

]

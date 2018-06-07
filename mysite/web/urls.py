from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'login/', views.login, name="login_page"),
    url(r'logout/', views.logout, name="logout"),
    url(r'register/', views.register, name="register_page"),
    url(r'logrequired/', views.login_require_page, name="logrequired"),
    url(r'index/', views.index, name="index"),
<<<<<<< HEAD
    url(r'register/create_code/',views.create_code_img,name="create_code"),
=======
    url(r'^create_code/', views.create_code_img),
    url(r'uploadvideo/', views.upload_video),
>>>>>>> 873451fdfe00eabd416b3f83e9cc4267fadcd75b

]

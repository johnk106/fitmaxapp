from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'fitMax'
urlpatterns = [
    path('',views.index,name = 'index'),
    path('pay/',views.pay,name = 'pay'),
    path('auth/login',views._login,name = 'login'),
    path('auth/sign-up/',views.sign_up,name = 'sign_up'),
    path('auth/logout',views.logout_view,name = 'logout'),
    path('login-required/',views.required,name = 'login-required'),
    path('checkout/',views.checkout,name='checkout')
]
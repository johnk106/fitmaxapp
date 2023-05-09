from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'fitMax'
urlpatterns = [
    path('',views.index,name = 'index'),
    path('pay/',views.pay,name = 'pay')
]
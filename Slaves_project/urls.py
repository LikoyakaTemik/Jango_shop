# django_auth/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', include('users.urls')),
    path('', views.home, name="home"),
    path("new_product/", views.new_product),
    path('account/', views.account, name="account"),
    path('shopping_cart/', views.shopping_cart, name="shopping_cart"),
    path('sc/', views.add_sc, name="add_sc"),
    path('room/', views.room, name="room"),
    path('chat_input/', views.chat_input),
    path('chat_list/', views.chat_list),
    path('create_chat/', views.create_chat, name="create_chat"),
]
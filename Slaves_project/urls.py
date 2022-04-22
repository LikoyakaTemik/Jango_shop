
from django.contrib import admin
from django.urls import path, include
from slave_site import views
from django.contrib.auth.views import LoginView
from slave_site.views import SignUpView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index_page, name="home"),
    path("catalog/", views.catalog_page),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', SignUpView.as_view(), name='signup')
]

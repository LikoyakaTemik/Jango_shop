
from django.contrib import admin
from django.urls import path
from slave_site import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index_page),
]

from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.listNews, name='listNews'),
    path('result', views.searchNews, name='searchNews'),
]
from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.listNews, name='listNews'),
    path('search/result', views.searchNews, name='searchNews'),
    path('search', views.searchView, name='search'),
    path('together', views.listNewsOnHTML, name='listNewsOnHTML'),
    path('together/result', views.searchNewsOnHTML, name='searchNewsOnHTML'),
]
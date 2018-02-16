from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.models, name='index'),
    url(r'^scoring/', views.scoring, name='index'),
    url(r'^concreteness_scoring/', views.concreteness_scoring, name='index'),
    url(r'^pictures_scoring/', views.pictures_scoring, name='index')
]
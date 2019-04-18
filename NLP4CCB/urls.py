from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.models, name="index"),
    url(r"^scoring/", views.scoring, name="index"),
]

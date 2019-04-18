"""NLP4CCB_Django_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from NLP4CCB.views import (
    confirmation,
    confirmation_scoring,
    index,
    leaderboard,
    signin,
    signout,
    signup,
)

urlpatterns = [
    url(r"^$", index),
    url(r"^models/", include("NLP4CCB.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^signin/", signin),
    url(r"^signout/", signout),
    url(r"^signup/", signup),
    url(r"^leaderboard/", leaderboard),
    url(r"^confirmation/", confirmation),
    url(r"^conf_scoring", confirmation_scoring),
]

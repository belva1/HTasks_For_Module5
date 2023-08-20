"""
URL configuration for VBproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.shortcuts import render


urlpatterns = [
    path('', views.articles_view, name='main_page'),
    path('about/', views.about_view, name='about_view'),

    path('profile/<str:username>/', views.profile_view, name='profile_page'),
    path('change-userdata/', views.ChangeUserDataView.as_view(), name='change_user_data_page'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('register/', views.register_view, name='register_page'),
    path('deactivate/', views.deactivate_view, name='deactivate_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),

    re_path(r'archive\/(?P<year>\d{4})\/(?P<month>0?[1-9]|1[0-2])\/', views.archive_view),

    path('topics/', views.topics_view, name='topics_view'),
    path('topics/<str:topic>/', views.topic_view, name='topic_view'),
    path('topics/<str:topic>/subscribe/', views.topic_subscribe_view),
    path('topics/<str:topic>/unsubscribe/', views.topic_unsubscribe_view),

    path('denied/', views.update_denied, name='update_denied'),
    path('<str:title_article>/', views.article_view, name='article_view'),
    path('article/create/', views.article_create_view, name='create_page'),
    path('<str:title_article>/update/', views.article_update_view, name='update_page'),
    path('<str:article>/delete/', views.article_delete_view),
    path('<str:article>/comment/', views.article_default_comment_view),
]
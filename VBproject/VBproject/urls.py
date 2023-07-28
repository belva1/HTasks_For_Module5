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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view),
    path('about/', views.descp_view),
    path('create/', views.create_view),

    path('profile/<str:username>/', views.profile_view),
    path('set-userdata/', views.set_user_data_view),
    path('set-password/', views.set_password_view),
    path('register/', views.register_view),
    path('deactivate/', views.deactivate_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),

    path('topics/', views.topics_view),
    path('topics/<str:topic>/subscribe/', views.topic_subscribe_view),
    path('topics/<str:topic>/unsubscribe/', views.topic_unsubscribe_view),

    path('archive/<int:year>/<int:month>/', views.archive_view),

    path('<str:article>/', views.article_view),
    path('<str:article>/update/', views.article_update_view),
    path('<str:article>/delete/', views.article_delete_view),
    path('<str:article>/comment/', views.article_default_comment_view),
    path('<str:article>/comment/<str:comment>/', views.article_comment_create_view),   
]
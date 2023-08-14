from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import ArticleForm, AuthUserForm, RegisterUserForm, ChangePasswordForm, ChangeUserDataForm
from .models import Article, Comment, UserModel, Topic
from .services import get_topics


def articles_view(request):
    template = 'article_components/articles_view.html'

    articles = Article.objects.annotate(comment_count=Count('comment'))
    context = {
        'articles': articles,
    }
    return render(request, template, context)


def about_view(request):
    template = 'article_components/about_view.html'
    return render(request, template)


def article_view(request, title_article):
    try:
        article_obj: Article = Article.objects.get(title=title_article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')

    template = 'article_components/article_view.html'
    comments = Comment.objects.filter(article_comment__title=article_obj)
    context = {
        'article_obj': article_obj,
        'comments': comments,
    }
    return render(request, template, context)


def article_create_view(request):
    template = 'article_components/create_page.html'
    context = {
        'form': ArticleForm(),
    }
    return render(request, template, context)


def article_update_view(request, title_article):
    template = 'article_components/update_page.html'
    try:
        get_article = Article.objects.get(title=title_article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')

    # if request.method == 'POST':
    #     form = ArticleForm(request.POST, instance=get_article)
    #     if form.is_valid():
    #         form.save()

    context = {
        'get_article': get_article,
        'update': True,
        'form': ArticleForm(instance=get_article),
    }

    return render(request, template, context)


def article_delete_view(request, article):
    template = 'article_components/article_view.html'
    try:
        get_article = Article.objects.get(title=article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')

    context = {
        'get_article': get_article,
        'delete': True,
    }
    return render(request, template, context)


def article_default_comment_view(request, article):
    try:
        current_article: Article = Article.objects.get(title=article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')
    article_comments = Comment.objects.filter(article_comment=current_article)
    comments: str = ''
    for comment in article_comments:
        comments += f"User: {comment.comment_author}\n\tComment: {comment.message}\n\n"
    return HttpResponse(comments, content_type="text/plain")


def topics_view(request):
    template = 'article_components/topics_view.html'
    topics = Topic.objects.all()
    topic_details: str = ''
    for topic in topics:
        topic_details += f"Title: {topic.title}\nDescription: {topic.description}\n\n"
    return render


def topic_view(request, topic):
    template = 'article_components/topic_view.html'
    try:
        topic = Topic.objects.get(title=topic)
    except Topic.DoesNotExist:
        raise Http404
    topic_article = Article.objects.filter(topic=topic)
    context = {
        'topic': topic,
        'topic_article': topic_article,
    }
    return render(request, template, context)


def topic_subscribe_view(request, topic):
    try:
        Topic.objects.get(title=topic)
    except Topic.DoesNotExist:
        raise Http404('Topic with this title does not exist.')
    return HttpResponse(f'Subscribe for {topic}.')


def topic_unsubscribe_view(request, topic):
    try:
        Topic.objects.get(title=topic)
    except Topic.DoesNotExist:
        raise Http404('Topic with this title does not exist.')
    return HttpResponse(f'Unsubscribe for {topic}.')


def profile_view(request, username) -> HttpResponse:
    template = 'user_components/profile_page.html'
    #  Here, instead of intercepting with an exception, I decided to use the method get_object_or_404
    user: UserModel = get_object_or_404(UserModel, username=username)
    list_of_preferred_topics = get_topics(user)
    # if not list_of_preferred_topics:
    #     list_of_preferred_topics = ['No preferred topics.']
    user_articles_list = Article.objects.filter(article_author=user)
    context = {
        'user_components': user,
        'list_of_preferred_topics': list_of_preferred_topics,
        'user_articles_list': user_articles_list,
    }
    return render(request, template, context)


class ChangeUserDataView(UpdateView):
    template_name = 'user_components/change_user_data_page.html'
    form_class = ChangeUserDataForm
    success_url = reverse_lazy('change_user_data_page')
    model = User

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(View):
    template_name = 'user_components/change_password_page.html'
    form_class = ChangePasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #
    #         return redirect('set_password_page')
    #     return render(request, self.template_name, {'form': form})


class RegisterView(CreateView):
    model = User
    template_name = 'user_components/register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_page')

# def register_view(request: HttpRequest):
#     template = 'register_page.html'
#     context = {
#
#     }
#     return render(request, template, context)


def deactivate_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Deactivate Form.')


class LoginView(LoginView):
    template_name = 'user_components/login_page.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('login_page')

# def login_view(request: HttpRequest) -> HttpResponse:
#     template = 'login_page.html'
#     context = {
#         'form': ,
#     }
#     return render(request, template, context)


def logout_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Logout.')


def archive_view(request: HttpRequest, year: str, month: str) -> HttpResponse:
    return HttpResponse(f'Archive: year - {year}, month - {int(month)}.')

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import ArticleForm, LoginViewForm,  ChangePasswordForm, ChangeUserDataForm, RegisterViewForm
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
    if not request.user.is_authenticated:
        url = reverse('login_view')
        return HttpResponseRedirect(url)
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

    if get_article.article_author != request.user:
        url = reverse('update_denied')
        return HttpResponseRedirect(url)

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


def update_denied(request):
    template = 'article_components/update_denied.html'
    return render(request, template)


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
    user_articles_list = Article.objects.filter(article_author=user)
    context = {
        'user_components': user,
        'list_of_preferred_topics': list_of_preferred_topics,
        'user_articles_list': user_articles_list,
    }
    return render(request, template, context)


class ChangeUserDataView(View):
    template_name = 'user_components/change_user_data_page.html'
    form_class = ChangeUserDataForm
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login_view')
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = self.form_class(user_data)
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={'username': self.request.user.username})

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login_view')

        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())

        return render(request, self.template_name, {'form': form})


class ChangePasswordView(View):
    template_name = 'user_components/change_password_page.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('login_view')

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login_view')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.change_password(request.user)
            # Redirect to the success URL after successful password change
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


def register_view(request):
    template = 'user_components/register_page.html'
    if request.method == 'POST':
        form = RegisterViewForm(request.POST)
        if form.is_valid():
            form.create_user()
            url = reverse('login_view')
            return HttpResponseRedirect(url)
    else:
        form = RegisterViewForm()
    return render(request, template, {'form': form})


def deactivate_view(request):
    user = request.user
    user.is_active = False
    user.save()
    url = reverse('login_view')
    return HttpResponseRedirect(url)


def login_view(request):
    template = 'user_components/login_page.html'
    if request.method == 'POST':
        form = LoginViewForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)  # return data, clean the form
            login(request, user)
            url = reverse('profile_page', kwargs={'username': user.username})
            return HttpResponseRedirect(url)
    else:
        form = LoginViewForm()
    return render(request, template, {'form': form})


def logout_view(request):
    url = reverse('login_view')
    logout(request)
    return HttpResponseRedirect(url)


def archive_view(request: HttpRequest, year: str, month: str) -> HttpResponse:
    return HttpResponse(f'Archive: year - {year}, month - {int(month)}.')
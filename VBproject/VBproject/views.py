from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from project_app.models import Article, Comment, UserModel, Topic
from project_app.services import get_topics


def articles_view(request: HttpRequest) -> HttpResponse:
    articles: list = Article.objects.all()  # querySet
    articles_info: str = ""
    for article in articles:
        articles_info += f"User: {article.article_author}\nTitle: {article.title}\nContent: {article.content}\nCreated at: {article.created_at}\nUpdated at: {article.updated_at}\n\n"
    return HttpResponse(articles_info, content_type="text/plain")


def descp_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('The site for first hw with Django.')


def create_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('FORM.')


def article_view(request: HttpRequest, title_article: str) -> HttpResponse:
    try:
        article_obj: Article = Article.objects.get(title=title_article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')

    comments: list = Comment.objects.filter(article_comment__title=article_obj)  # querySet
    article_details: str = f"Title: {article_obj.title}\nContent: {article_obj.content}\nCreated at: {article_obj.created_at}\nUpdated at: {article_obj.updated_at}\nComments:\n"
    """
        To append the value of a class object field in the string
        the message is added to the main string during the execution of the cycle
    """
    for comment in comments:
        article_details += f"  - {comment.message}\n"
    return HttpResponse(article_details, content_type="text/plain")


def article_update_view(request: HttpRequest, title_article) -> HttpResponse:
    try:
        Article.objects.get(title=title_article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')

    return HttpResponse('Form for update.')


def article_delete_view(request: HttpRequest, article: str) -> HttpResponse:
    try:
        Article.objects.get(title=article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')

    return HttpResponse('Confirmation for delete.')


def article_default_comment_view(request: HttpRequest, article: str) -> HttpResponse:
    try:
        current_article: Article = Article.objects.get(title=article)
    except Article.DoesNotExist:
        raise Http404('Article with this title does not exist.')
    article_comments: list = Comment.objects.filter(article_comment=current_article)  # querySet
    comments: str  = ''
    for comment in article_comments:
        comments += f"User: {comment.comment_author}\n\tComment: {comment.message}\n\n"
    return HttpResponse(comments, content_type="text/plain")


def topics_view(request: HttpRequest) -> HttpResponse:
    topics: list = Topic.objects.all()
    topic_details: str = ''
    for topic in topics:
        topic_details += f"Title: {topic.title}\nDescription: {topic.description}\n\n"
    return HttpResponse(topic_details, content_type="text/plain")


def topic_subscribe_view(request: HttpRequest, topic: str) -> HttpResponse:
    try:
        Topic.objects.get(title=topic)
    except Topic.DoesNotExist:
        raise Http404('Topic with this title does not exist.')
    return HttpResponse(f'Subscribe for {topic}.')


def topic_unsubscribe_view(request: HttpRequest, topic: str) -> HttpResponse:
    try:
        Topic.objects.get(title=topic)
    except Topic.DoesNotExist:
        raise Http404('Topic with this title does not exist.')
    return HttpResponse(f'Unsubscribe for {topic}.')


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    #  Here, instead of intercepting with an exception, I decided to use the method get_object_or_404
    user: UserModel = get_object_or_404(UserModel, username=username)
    list_of_preferred_topics = get_topics(user)
    if list_of_preferred_topics == '':
        list_of_preferred_topics = 'No preferred topics.'
    user_articles_list: list = Article.objects.filter(article_author=user)  # querySet
    user_articles: str = ''
    for article in user_articles_list:
        user_articles += f"Title: {article.title}\nContent: {article.content}\n\n"
    return HttpResponse(f"User: {user}\n\n\nArticles on preferred topics:\n{list_of_preferred_topics}\n\nARTICLES\n\n{user_articles}", content_type="text/plain")


def set_user_data_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Set User Data.')


def set_password_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Set Password.')


def register_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Register Form.')


def deactivate_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Deactivate Form.')


def login_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Login.')


def logout_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Logout.')


def archive_view(request: HttpRequest, year: str, month: str) -> HttpResponse:
    return HttpResponse(f'Archive: year - {year}, month - {int(month)}.')

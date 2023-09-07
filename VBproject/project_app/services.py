from .models import UserModel, Topic, TopicUser, Article


def get_topics(user: UserModel) -> list:
    preferred_topic: list = TopicUser.objects.filter(user=user).values_list('topic__title', flat=True)
    articles = Article.objects.filter(topic__title__in=preferred_topic).values_list('title', flat=True)
    return articles
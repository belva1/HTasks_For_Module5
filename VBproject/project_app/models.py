from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
UserModel = get_user_model()  # table of users


class Topic(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=255)
    topic_user = models.ManyToManyField(UserModel, through='TopicUser')


class TopicUser(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    topic_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notify_field = models.BooleanField(default=False)


class Article(models.Model):
    header = models.TextField(max_length=255)
    contain = models.TextField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    article_author = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # author field in the Article table
    article_topic = models.ManyToManyField('Topic', through='ArticleTopic')


class ArticleTopic(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date_join = models.DateField(auto_now_add=True)


class Comment(models.Model):
    created_at = models.DateField(auto_now_add=True)
    notification = models.TextField()
    comment_author = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # author field in the Comment table
    article_comment = models.ForeignKey(Article, on_delete=models.CASCADE)


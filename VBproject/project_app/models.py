from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

UserModel = get_user_model()  # table of users


class Topic(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=255)
    topic_user = models.ManyToManyField(UserModel, through='TopicUser')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'id']


class TopicUser(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    notify = models.BooleanField(default=False)


class Article(models.Model):
    title = models.TextField(max_length=64, unique=True)
    content = models.TextField(validators=[MinLengthValidator(255)])
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    topic = models.ManyToManyField(Topic)
    article_author = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # author field in the Article table

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', 'id']


class Comment(models.Model):
    created_at = models.DateField(auto_now_add=True)
    message = models.TextField()
    comment_author = models.ForeignKey(UserModel, on_delete=models.CASCADE)  # author field in the Comment table
    article_comment = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['created_at', 'id']
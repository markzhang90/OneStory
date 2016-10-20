from django.db import models
# Create your models here.


class UserProfile(models.Model):

    passid = models.CharField(max_length=255, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField(unique=True)
    update_time = models.DateTimeField(auto_now=True)
    nick_name = models.CharField(blank=True, max_length=255)
    ext = models.TextField(blank=True, default='')

    def __str__(self):
        return str(self.email)


class Article(models.Model):

    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True)
    ext = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    status = models.SmallIntegerField(default=1)

    def __str__(self):
        return str(self.pk)


class Comment(models.Model):

    reply_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reply_previous = models.BigIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    status = models.SmallIntegerField(default=1)
    ext = models.TextField(blank=True)

    def __str__(self):
        return str(self.pk)

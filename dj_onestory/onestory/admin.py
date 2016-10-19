from django.contrib import admin

from .models import Article, Comment, UserProfile
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author_passid', 'title', 'create_date', 'update_time', 'link', 'status')
    empty_value_display = '-empty-'

    def author_passid(self, obj):
        return obj.author.passid


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('passid', 'email', 'phone', 'update_time', 'nick_name', 'ext')
    empty_value_display = '-empty-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('article_id', 'author_passid', 'reply_previous', 'create_date', 'content', 'status')
    empty_value_display = '-empty-'

    def author_passid(self, obj):
        return obj.author.passid

    def article_id(self, obj):
        return obj.reply_article.pk

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
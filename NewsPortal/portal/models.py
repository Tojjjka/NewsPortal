from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating_article = self.post_set.aggregate(sra=Coalesce(Sum('news_rating'), 0)).get('sra')
        sum_rating_comment_author = self.user.comment_set.aggregate(srca=Coalesce(Sum('comment_rating'), 0)).get('srca')
        sum_rating_comment_all_article = self.post_set.aggregate(srcaa=Coalesce(Sum('comment__comment_rating'), 0)).get('srcaa')
        self.rating = (sum_rating_article * 3) + sum_rating_comment_author + sum_rating_comment_all_article
        self.save()


class Category(models.Model):
    name_category = models.TextField(max_length=30, unique=True)


class Post(models.Model):
    article = 'ART'
    news = 'NEW'

    SELECTION_FIELD = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice_field = models.CharField(max_length=3, choices=SELECTION_FIELD, default=news)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    news_headline = models.TextField(max_length = 255)
    news_text = models.TextField(max_length=255)
    news_rating = models.IntegerField(default=0)

    def like(self):
        self.news_rating += 1
        self.save()

    def dislike(self):
        self.news_rating += 1
        self.save()

    def preview(self):
        return f'{self.news_text[:125]}...'



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    Category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating += 1
        self.save()


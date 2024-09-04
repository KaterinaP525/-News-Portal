from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    raiting_author = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = sum(post.post_rating * 3 for post in self.post_set.all())
        comment_rating = sum(comment.comment_rating for post in self.post_set.all() for comment in post.comment_set.all())
        author_comments = sum(comment.comment_rating for comment in Comment.objects.filter(user=self.user))
        self.raiting_author = post_rating + comment_rating + author_comments
        self.save()

class Category (models.Model):
    name = models.CharField(max_length=80, unique=True)

class Post(models.Model):
    POST_CHOICES = [
        ('news', 'news'),
        ('post', 'post')
    ]
    post_type = models.CharField(choices=POST_CHOICES, max_length=100)
    creations = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


    def preview(self):
        if len(self.text) > 124:
            return self.text[:124] + '...'
        else:
            return self.text

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)





from django.db import models
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.utils import timezone
from django.utils.html import strip_tags


class User(models.Model):
    username = models.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[\w.-]+$', 'Введите только латинские буквы, цифры, точки и дефисы')],
        unique=True
    )
    email = models.EmailField(validators=[EmailValidator()])
    home_page = models.URLField(validators=[URLValidator()], blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self):
        self.likes += 1
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def clean(self):
        self.text = strip_tags(self.text)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.save()

    class Meta:
        ordering = ['-created_at']

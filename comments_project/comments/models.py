from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.utils import timezone
from django.utils.html import strip_tags


class CustomUserManager(BaseUserManager):
    def create_user(self, email, login, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not login:
            raise ValueError('The Login field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, login=login, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, login, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[\w.-]+$', 'Введите только латинские буквы, цифры, точки и дефисы')],
        unique=True
    )
    login = models.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[\w.-]+$', 'Введите только латинские буквы, цифры, точки и дефисы')],
        unique=True
    )
    home_page = models.URLField(validators=[URLValidator()], blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'login']

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.likes -= 1
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def clean(self):
        self.text = strip_tags(self.text)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.likes -= 1
        self.save()

    class Meta:
        ordering = ['-created_at']

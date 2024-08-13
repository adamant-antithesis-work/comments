import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.views import View
from django.views.generic import ListView, FormView
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user': RegisterSerializer(user).data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'redirect_url': '/'
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            root_comments = post.comments.filter(parent__isnull=True)
            post.root_comments = root_comments

            paginator = Paginator(root_comments, 25)
            page_number = self.request.GET.get(f'comments_page_{post.id}', 1)
            page_obj = paginator.get_page(page_number)
            post.page_obj = page_obj

        comment_form = CommentForm(request=self.request)
        context['comment_form'] = comment_form
        context['captcha_image'] = comment_form.captcha_image

        return context


class AddCommentView(LoginRequiredMixin, FormView):
    template_name = 'add_comment.html'
    form_class = CommentForm
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['post'] = post
        context['parent_id'] = self.request.GET.get('parent_id')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.post = post
        comment.user = self.request.user

        user = self.request.user
        new_email = form.cleaned_data.get('email')
        new_home_page = form.cleaned_data.get('home_page')

        if new_email and user.email != new_email:
            user.email = new_email

        if new_home_page and user.home_page != new_home_page:
            user.home_page = new_home_page

        try:
            comment.save()

            if 'avatar' in self.request.FILES:
                avatar = self.request.FILES['avatar']
                filename = f'user_{comment.user.id}_{comment.id}.jpg'
                filepath = os.path.join(settings.MEDIA_ROOT, 'avatars', filename)
                with open(filepath, 'wb+') as f:
                    f.write(avatar.read())
                comment.user.avatar = filename

            user.save()
        except IntegrityError as e:
            if 'email' in str(e):
                form.add_error('email', 'Этот email уже используется другим пользователем.')
            else:
                form.add_error(None, 'Ошибка при сохранении комментария.')
            return self.form_invalid(form)

        return redirect('post-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LikeDislikeView(View):
    def post(self, request, content_id, content_type, action):
        if content_type == 'post':
            content = get_object_or_404(Post, id=content_id)
        elif content_type == 'comment':
            content = get_object_or_404(Comment, id=content_id)
        else:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if action == 'like':
            content.likes += 1
        elif action == 'dislike':
            if content.likes > 0:
                content.likes -= 1
        content.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

import os

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
from django.http import JsonResponse
from django.views import View
from .forms import CommentForm, RegisterForm


def render_error_template(request):
    error_message = request.POST.get('error_message', 'Unknown error')
    return JsonResponse({'error_message': error_message})


class LogoutView(DjangoLogoutView):
    next_page = '/'


class ErrorPageView(View):
    def get(self, request):
        return render(request, 'error.html')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('post-list'))
        else:
            error_messages = []
            for field, errors in form.errors.items():
                field_errors = []
                for error in errors:
                    if isinstance(error, dict):
                        message = error.get('message', 'Unknown error')
                    else:
                        message = str(error)
                    field_errors.append(message)
                field_errors_str = '; '.join(field_errors)
                error_messages.append(f"{field.capitalize()}: {field_errors_str}")

            error_message = ' | '.join(error_messages)

            return redirect(f'{reverse("error_page")}?{urlencode({"error_message": error_message})}')


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login = serializer.validated_data['login']
            password = serializer.validated_data['password']

            user = authenticate(request, login=login, password=password)
            if user is not None:
                auth_login(request, user)
                refresh = RefreshToken.for_user(user)
                response = redirect('/')
                response.set_cookie('refresh', str(refresh))
                response.set_cookie('access', str(refresh.access_token))
                return response
            else:
                return redirect(f'{reverse("error_page")}?{urlencode({"error_message": "Invalid credentials"})}')
        else:
            errors = serializer.errors
            error_message = "; ".join(f"{field}: {', '.join(msg for msg in error_list)}" for field, error_list in errors.items())
            return redirect(f'{reverse("error_page")}?{urlencode({"error_message": error_message})}')


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            root_comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
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

            if 'attachment' in self.request.FILES:
                attachment = self.request.FILES['attachment']
                filename = f'comment_{comment.id}_{attachment.name}'
                filepath = os.path.join(settings.MEDIA_ROOT, 'attachments', filename)
                with open(filepath, 'wb+') as f:
                    f.write(attachment.read())
                comment.attachment = filename

            user.save()
        except IntegrityError as e:
            if 'email' in str(e):
                form.add_error('email', 'Этот email уже используется другим пользователем.')
            else:
                form.add_error(None, 'Ошибка при сохранении комментария.')
            return self.form_invalid(form)

        return redirect('post-list')

    def form_invalid(self, form):
        errors = form.errors
        error_message = "; ".join(
            f"{field}: {', '.join(msg for msg in error_list)}" for field, error_list in errors.items())
        return redirect(f'{reverse("error_page")}?{urlencode({"error_message": error_message})}')


class LikeDislikeView(View):
    def post(self, request, content_id, content_type, action):
        if content_type == 'post':
            content = get_object_or_404(Post, id=content_id)
        elif content_type == 'comment':
            content = get_object_or_404(Comment, id=content_id)
        else:
            return JsonResponse({'success': False})

        if action == 'like':
            content.likes += 1
        elif action == 'dislike':
            content.likes -= 1
        content.save()

        return JsonResponse({'success': True, 'likes': content.likes})

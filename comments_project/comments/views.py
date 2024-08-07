from django.views.generic import ListView, FormView
from django.shortcuts import get_object_or_404, redirect
from .models import Post, User
from .forms import CommentForm, UserForm


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm()
        context['comment_form'] = CommentForm()
        return context


class AddCommentView(FormView):
    template_name = 'add_comment.html'
    form_class = CommentForm
    second_form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['user_form'] = self.second_form_class()
        context['comment_form'] = self.form_class()
        context['post'] = post
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        user_form = self.second_form_class(self.request.POST)
        comment_form = self.form_class(self.request.POST)

        if user_form.is_valid() and comment_form.is_valid():
            user, created = User.objects.get_or_create(
                username=user_form.cleaned_data['username'],
                defaults={'email': user_form.cleaned_data['email'], 'home_page': user_form.cleaned_data['home_page']}
            )
            if not created:
                user.email = user_form.cleaned_data['email']
                user.home_page = user_form.cleaned_data['home_page']
                user.save()

            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return redirect('post-list')
        else:
            return self.form_invalid(user_form, comment_form)

    def form_invalid(self, user_form, comment_form):
        return self.render_to_response(self.get_context_data(user_form=user_form, comment_form=comment_form))

from django.views.generic import ListView
from .models import Post, Comment


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 25

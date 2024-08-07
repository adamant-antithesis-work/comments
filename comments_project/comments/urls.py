from django.urls import path
from .views import PostListView, AddCommentView, LikeCommentView, DislikeCommentView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('add-comment/<int:post_id>/', AddCommentView.as_view(), name='add-comment'),
    path('like-comment/<int:comment_id>/', LikeCommentView.as_view(), name='like-comment'),
    path('dislike-comment/<int:comment_id>/', DislikeCommentView.as_view(), name='dislike-comment'),
]

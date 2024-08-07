from django.urls import path
from .views import PostListView, AddCommentView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('add-comment/<int:post_id>/', AddCommentView.as_view(), name='add-comment'),
]

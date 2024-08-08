from django.urls import path
from .views import PostListView, AddCommentView, RegisterView, LoginView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('add-comment/<int:post_id>/', AddCommentView.as_view(), name='add-comment'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

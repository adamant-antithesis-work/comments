from django.urls import path
from .views import PostListView, AddCommentView, RegisterView, LoginView, LikeDislikeView, ErrorPageView, LogoutView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('add-comment/<int:post_id>/', AddCommentView.as_view(), name='add-comment'),
    path('like-dislike/<int:content_id>/<str:content_type>/<str:action>/', LikeDislikeView.as_view(), name='like-dislike'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('error/', ErrorPageView.as_view(), name='error_page'),
]

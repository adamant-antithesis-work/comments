from django import forms
from .models import Comment, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'home_page']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }

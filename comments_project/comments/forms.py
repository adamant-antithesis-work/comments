import os
from django import forms
from django.conf import settings

from .captcha_utils import generate_captcha
from .models import Comment, User


class CommentForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    home_page = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your homepage (optional)'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your comment',
            'style': 'height: 100px;'
        })
    )
    avatar = forms.ImageField(required=False)
    captcha_text = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter CAPTCHA'
        })
    )
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Comment
        fields = ['username', 'email', 'home_page', 'text', 'avatar',  'captcha_text', 'parent']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.captcha_dir = os.path.join(settings.BASE_DIR, 'static', 'captcha')
        self.captcha_text, self.captcha_image = self.get_captcha()

        self.fields['text'].widget.attrs.update({'class': 'form-control'})

    def get_captcha(self):
        captcha_files = [f for f in os.listdir(self.captcha_dir) if os.path.isfile(os.path.join(self.captcha_dir, f))]

        if captcha_files:
            captcha_image = captcha_files[0]
            captcha_text = captcha_image.replace('captcha_', '').replace('.png', '')
            return captcha_text, captcha_image
        else:
            return generate_captcha()

    def clean(self):
        cleaned_data = super().clean()
        captcha_text = cleaned_data.get('captcha_text', '')

        expected_captcha_text = self.captcha_text

        if captcha_text.upper() != expected_captcha_text:
            self.add_error('captcha_text', 'Неверная CAPTCHA')

        captcha_image_path = os.path.join(self.captcha_dir, self.captcha_image)
        if os.path.exists(captcha_image_path):
            os.remove(captcha_image_path)

        return cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['login', 'username', 'email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'login': forms.TextInput(attrs={'placeholder': 'Enter your login'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            self.add_error('password2', "Passwords do not match")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

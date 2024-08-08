import os

from django import forms
from rest_framework.exceptions import ValidationError
from django.conf import settings

from .captcha_utils import generate_captcha
from .models import Comment, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'home_page']


class CommentForm(forms.ModelForm):
    captcha_text = forms.CharField(max_length=6, required=True)
    parent = forms.ModelChoiceField(queryset=Comment.objects.all(), required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ['text', 'captcha_text', 'parent']

    class Meta:
        model = Comment
        fields = ['text', 'captcha_text']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.captcha_dir = os.path.join(settings.BASE_DIR, 'static', 'captcha')

        self.captcha_text, self.captcha_image = self.get_captcha()

        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['captcha_text'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter CAPTCHA'
        })

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
            raise ValidationError("Invalid CAPTCHA")

        captcha_image_path = os.path.join(self.captcha_dir, self.captcha_image)
        if os.path.exists(captcha_image_path):
            os.remove(captcha_image_path)

        return cleaned_data

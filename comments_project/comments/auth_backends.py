from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class LoginBackend(BaseBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(login=login)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

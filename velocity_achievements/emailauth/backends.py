from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from emailauth.models import UserWithEmail

class EmailBackend(ModelBackend):
    object_class = UserWithEmail
    def authenticate(self, email, password):
        try:
            user = self.object_class.objects.get(emails__email=email, is_active=True)
            if user.check_password(password):
                return user
            return None
        except self.object_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.object_class.objects.get(pk=user_id)
        except self.object_class.DoesNotExist:
            return None

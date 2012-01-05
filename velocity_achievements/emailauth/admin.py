from django.contrib.admin import ModelAdmin, site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from models import UserWithEmail, EmailAddress, ActivationEmail

class UserWithEmailChangeForm(UserChangeForm):
    pass

class UserWithEmailAdmin(UserAdmin):
    pass

site.register(UserWithEmail, UserWithEmailAdmin)
site.register(EmailAddress, ModelAdmin)
site.register(ActivationEmail, ModelAdmin)

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from models import UserWithEmail, EmailAddress, ActivationEmail

attrs_dict = {}

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    email/password logins.
    """
    email = forms.EmailField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct email and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class PasswordInitialSetForm(forms.Form):
    token = forms.ModelChoiceField(queryset = ActivationEmail.objects.active(), widget = forms.HiddenInput)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u'password'))
    password_confirmation = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u'password confirmation'))

    def clean_password_confirmation(self):
        password1 = self.cleaned_data.get("password", "")
        password2 = self.cleaned_data["password_confirmation"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields did not match."))
        return password2

    def save(self, commit=True):
        activation = self.cleaned_data['token']
        user = activation.user
        password = self.cleaned_data["password"]
        user.set_password(password)
        user.is_active = True
        activation.activate()
        authenticate(email = user.primary_email.email, password = password)
        user.save()
        return user

"""
class PasswordResetRequestForm(forms.Form):
    email = forms.ModelChoiceField(label=_(u'your email address'), queryset=EmailAddress.objects.all())

    def clean_email(self):
        data = self.cleaned_data
        try:
            user_email = EmailAddress.objects.get(email=data['email'])
            return data['email']
        except EmailAddress.DoesNotExist:
            raise forms.ValidationError(_(u'Unknown email'))


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
        label=_(u'password (again)'))
    
    clean_password2 = clean_password2


class AddEmailForm(forms.Form):
    email = forms.EmailField(label=_(u'new email address'))

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            user = UserEmail.objects.get(email=email)
            raise forms.ValidationError(_(u'This email is already taken.'))
        except UserEmail.DoesNotExist:
            pass
        return email
"""

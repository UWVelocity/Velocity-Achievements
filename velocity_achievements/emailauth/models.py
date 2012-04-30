from django.db import models, transaction
from django.template.loader import render_to_string
from django.contrib.auth.models import User, UserManager
from django.contrib.sites.models import Site
from django.conf import settings
from django.core import mail
import string
import random
import datetime

def nested_commit_on_success(func):
    """Like commit_on_success, but doesn't commit existing transactions.

    This decorator is used to run a function within the scope of a 
    database transaction, committing the transaction on success and
    rolling it back if an exception occurs.

    Unlike the standard transaction.commit_on_success decorator, this
    version first checks whether a transaction is already active.  If so
    then it doesn't perform any commits or rollbacks, leaving that up to
    whoever is managing the active transaction.

    From http://djangosnippets.org/snippets/1343/
    """
    commit_on_success = transaction.commit_on_success(func)
    def _nested_commit_on_success(*args, **kwds):
        if transaction.is_managed():
            return func(*args,**kwds)
        else:
            return commit_on_success(*args,**kwds)
    return transaction.wraps(func)(_nested_commit_on_success)

def random_string(length, character_set = (string.ascii_letters + string.digits)):
    return ''.join(random.choice(character_set) for x in range(length))

def random_username(character_set = (string.ascii_letters + string.digits)):
    return 'AUTO_' + random_string(25, character_set)

class UserWithEmailManager(UserManager):
    @nested_commit_on_success
    def create_user(self, email, password = None, **kwargs):
        user = self.create(username = random_username(), email = email, **kwargs)
        user.set_password(password)
        user.send_activation_email(email, True)
        return user

class UserWithEmail(User):
    objects = UserWithEmailManager()

    def get_primary_email(self):
        return self.emails.get(primary = True)

    @nested_commit_on_success
    def set_primary_email(self, email_to_set):
        self.emails.filter(primary = True, pk__ne = email_to_set.pk).update(primary = False)
        self.emails.filter(primary = False, pk = email_to_set.pk).update(primary = True)

    primary_email = property(get_primary_email, set_primary_email)

    @nested_commit_on_success
    def send_activation_email(self, email, primary):
        email_address, created = EmailAddress.objects.get_or_create(email = email, defaults = dict(primary = primary, user = self))
        activation_email = ActivationEmail.objects.create(email = email_address, user = self)
        activation_email.send_activation()

    class Meta:
        verbose_name_plural = 'users with emails'

class EmailAddress(models.Model):
    email = models.EmailField(primary_key = True)
    user = models.ForeignKey(UserWithEmail, related_name = "emails")
    primary = models.BooleanField(default = False)
    
    class Meta:
        verbose_name_plural = 'email addresses'

def email_verification_days():
    return getattr(settings, 'EMAILAUTH_VERIFICATION_DAYS', 3)

class ActivationManager(models.Manager):
    def with_expiry(self, key):
        return self.filter(**{key: datetime.datetime.now() - datetime.timedelta(days = email_verification_days())})
    def active(self):
        return self.with_expiry('creation__gt')
    def expired(self):
        return self.with_expiry('creation__lt')
    def clean_expired(self):
        return self.expired().delete()

class ActivationEmail(models.Model):
    token = models.CharField(max_length = 40, default = lambda : random_string(40), primary_key = True)
    email = models.ForeignKey(EmailAddress, related_name = '+')
    user = models.ForeignKey(UserWithEmail, related_name = '+') # '+' means no reverse relation
    creation = models.DateTimeField(auto_now_add=True)

    objects = ActivationManager()

    @nested_commit_on_success
    def activate(self, password=None):
        if not self.valid:
            raise 
        self.email.user = self.user
        if password:
            self.user.set_password(password)
        self.user.save()
        self.email.save()
        self.delete()

    @property
    def valid(self):
        return datetime.datetime.now() < (self.creation + datetime.timedelta(days = email_verification_days()))

    def send_activation(self):
        current_site = Site.objects.get_current()
        
        subject = render_to_string('emailauth/verification_email_subject.txt', {'site': current_site})
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('emailauth/verification_email.txt', {
            'token': self.token,
            'expiration_days': email_verification_days(),
            'site': current_site,
        })

        mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email.email]) 


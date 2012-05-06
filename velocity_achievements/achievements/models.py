from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.dispatch import receiver
from convert import svg_to_png
import django.core.files.base as files
from emailauth.models import UserWithEmail, UserWithEmailManager
import tempfile
import datetime

def on_change(model, field_name):
    def callback(function):
        @receiver(pre_save, sender=model)
        def check(instance, **kwargs):
            if kwargs.get('raw', False):
                return
            try:
                old = model.objects.get(pk=instance.pk)
                old_value = getattr(old, field_name)
                new_value = getattr(instance, field_name)
                if old_value != new_value:
                    function(instance=instance, old_value=old_value, new_value=new_value)
            except model.DoesNotExist:
                pass
        return check
    return callback

class Achievement(models.Model):
    name = models.CharField(max_length = 128)
    description = models.CharField(max_length = 1024)
    can_nominate = models.BooleanField(default=True)

    svg_file = models.FileField(upload_to = "achievements")

    def thumbnail(self, width, height):
        render, created = self.render_set.get_or_create(width=width, height=height)
        return render

    @property
    def default_thumbnail(self):
        return self.thumbnail(100,100)

    def __unicode__(self):
        return self.name

@on_change(Achievement, 'svg_file')
def reset_renders(instance, **kwargs):
    instance.render_set.all().delete()

class Render(models.Model):
    achievement = models.ForeignKey(Achievement)
    width = models.IntegerField()
    height = models.IntegerField()
    image = models.ImageField(upload_to="achievements/thumbnails", height_field = "height", width_field = "width")

    def generate_image(self):
        svg = self.achievement.svg_file
        svg.open(mode='rb')
        try:
            image_data = svg_to_png(svg.read(), self.width, self.height)
            self.image.save("thumb.png", files.ContentFile(image_data), save=False)
        finally:
            svg.close()

    class Meta:
        unique_together = ("achievement", "width", "height")

@receiver(pre_save, sender=Render)
def generate(instance, **kwargs):
    if not instance.image:
        instance.generate_image()

class ParticipantManager(UserWithEmailManager):
    pass

class Participant(UserWithEmail):
    objects = ParticipantManager()
    achievements = models.ManyToManyField(Achievement, through='Grant')
    approved = models.BooleanField(default=False)

    @property
    def achievements(self):
        return Achievement.objects.filter(grant__participant = self,
                grant__term_id = Term.current_term_key()
                ).order_by("-grant__granted")

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.name

@receiver(post_save, sender=Participant)
def add_level1_achievement(instance, **kwargs):
    instance.grant_set.get_or_create(achievement = Achievement.objects.get(name = "LEVEL 1"))

term_choices = tuple(
        ('%s%s' % (term[0], year), '%s %s' % (term[1], year))
            for year in xrange(2011,2020)
            for term in (('W','Winter',), ('S','Spring',), ('F','Fall',))
        )

class TermQuerySet(QuerySet):
    def for_date(self,date):
        return self.filter(term=Term.term_key_for_date(date))
    def current(self):
        return self.for_date(datetime.date.today())

class TermManager(models.Manager):
    def get_query_set(self):
        return TermQuerySet(self.model)
    def for_date(self,date):
        return self.get_query_set().for_date(date)
    def current(self):
        return self.get_query_set().current()

class Term(models.Model):
    term = models.CharField(max_length=5, choices=term_choices, primary_key=True)

    def __unicode__(self):
        return self.get_term_display()

    @classmethod
    def term_key_for_date(cls,date):
        t="WSF"[(date.month - 1)/4] # Math is magic
        return t + str(date.year)

    @classmethod
    def current_term_key(cls):
        return cls.term_key_for_date(datetime.date.today())

    objects = TermManager()

class TermDependentQuerySet(QuerySet):
    def active(self):
        return self.filter(term_id=Term.current_term_key())

class TermDependentManager(models.Manager):
    def get_query_set(self):
        return TermDependentQuerySet(self.model)

    def active(self):
        return self.get_query_set().active()

class Nomination(models.Model):
    achievement = models.ForeignKey(Achievement)
    participant = models.ForeignKey(Participant)
    nominator = models.ForeignKey(Participant, related_name='+')
    term = models.ForeignKey(Term, default=Term.current_term_key)

    def granted(self):
        return bool(Grant.objects.filter(
            term=self.term,
            achievement=self.achievement,
            participant=self.participant,
            ))

    def clean(self):
        super(Nomination, self).clean()
        if self.participant_id and self.participant_id == self.nominator_id:
            raise ValidationError("Cannot nominate self.")
        if not self.achievement.can_nominate:
            raise ValidationError("This achievement does not accept nominations.")
        if Grant.objects.filter(achievement__pk = self.achievement_id,
                participant__pk = self.participant_id, term = self.term):
            raise ValidationError("This person has already been given this achievement this term.")
        if Nomination.objects.filter(achievement__pk = self.achievement_id, participant__pk = self.participant_id, nominator__pk = self.nominator_id, term = self.term).exclude(pk = self.pk).exists():
            raise ValidationError("Already nominated this person for this achievement this term.")

    class Meta:
        unique_together = ('achievement', 'participant', 'nominator','term',)

    objects = TermDependentManager()

class Grant(models.Model):
    achievement = models.ForeignKey(Achievement)
    participant = models.ForeignKey(Participant)
    granted = models.DateTimeField(auto_now_add=True)
    term = models.ForeignKey(Term, default=Term.current_term_key)

    def __unicode__(self):
        return "Grant %s to %s on %s" % (self.achievement_id, self.participant_id, self.granted)

    @property
    def nominated_by(self):
        return Participant.objects.filter(nomination__achievement = self.achievement, nomination__participant = self.participant)

    class Meta:
        unique_together = ('achievement', 'participant','term',)

    objects = TermDependentManager()

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.dispatch import receiver
from convert import svg_to_png
import django.core.files.base as files
from emailauth.models import UserWithEmail, UserWithEmailManager
import tempfile

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

    @property
    def achievements(self):
        return Achievement.objects.filter(grant__participant = self).order_by("-grant__granted")

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.name

@receiver(post_save, sender=Participant)
def add_level1_achievement(instance, **kwargs):
    instance.grant_set.get_or_create(achievement = Achievement.objects.get(name = "LEVEL 1"))

class Nomination(models.Model):
    achievement = models.ForeignKey(Achievement)
    participant = models.ForeignKey(Participant)
    nominator = models.ForeignKey(Participant, related_name='+')

    def clean(self):
        super(Nomination, self).clean()
        if self.participant_id and self.participant_id == self.nominator_id:
            raise ValidationError("Cannot nominate self.")
        if Grant.objects.filter(achievement__pk = self.achievement_id, participant__pk = self.participant_id):
            raise ValidationError("This person has already been given this achievement.")
        if Nomination.objects.filter(achievement__pk = self.achievement_id, participant__pk = self.participant_id, nominator__pk = self.nominator_id).exclude(pk = self.pk).exists():
            raise ValidationError("Already nominated this person for this achievement.")

    class Meta:
        unique_together = ('achievement', 'participant', 'nominator',)

class Grant(models.Model):
    achievement = models.ForeignKey(Achievement)
    participant = models.ForeignKey(Participant)
    granted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Grant %s to %s on %s" % (self.achievement_id, self.participant_id, self.granted)

    @property
    def nominated_by(self):
        return Participant.objects.filter(nomination__achievement = self.achievement, nomination__participant = self.participant)

    class Meta:
        unique_together = ('achievement', 'participant')

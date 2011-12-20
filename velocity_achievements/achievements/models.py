from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver
from convert import svg_to_png
import django.core.files.base as files
import tempfile

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

class Participant(User):
    @property
    def achievements(self):
        return Achievement.objects.filter(grant__participant = self).order_by("-grant__granted")

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.name

class Grant(models.Model):
    achievement = models.ForeignKey(Achievement)
    participant = models.ForeignKey(Participant)
    granted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Grant %s to %s on %s" % (self.achievement_id, self.participant_id, self.granted)

    class Meta:
        unique_together = ('achievement', 'participant')

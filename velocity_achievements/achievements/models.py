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


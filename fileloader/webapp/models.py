import wave

import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pydub import AudioSegment

from webapp.utils import build_config


def validate_wav(value):
    if not value.name.endswith(('.wav', '.mp3')):
        raise ValidationError('Неверный формат файла')


class WAVFile(models.Model):
    file = models.FileField(upload_to='.', validators=[validate_wav])
    number = models.CharField(verbose_name='DID номер', max_length=50)
    active = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super(WAVFile, self).__init__(*args, **kwargs)
        self.old_file = self.file

    def convert(self):
        if self.file.name.endswith('.mp3'):
            sound = AudioSegment.from_mp3(self.file.file)
            self.file = self.file.name.replace('.mp3', '.wav')
            self.save()
        else:
            sound = AudioSegment.from_wav(self.file.path)
        sound = sound.set_channels(1)
        sound = sound.set_frame_rate(8000)
        sound = sound.set_sample_width(2)
        sound.export(self.file.path, format="wav")

    @property
    def filename(self):
        return os.path.basename(self.file.name)


@receiver(post_save, sender=WAVFile)
def save(instance, created, **kwargs):
    build_config(WAVFile.objects.filter(active=True))

    if created:
        return

    if instance.old_file.name != instance.file.name and os.path.exists(instance.file.path):
        os.remove(instance.file.path)


@receiver(post_delete, sender=WAVFile)
def delete(instance, **kwargs):
    build_config(WAVFile.objects.filter(active=True))
    if os.path.exists(instance.file.path):
        os.remove(instance.file.path)

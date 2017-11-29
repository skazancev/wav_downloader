# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import wave

import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from webapp.utils import build_config

logger = logging.getLogger(__name__)


def validate_wav(value):
    if not value.name.endswith('.wav'):
        raise ValidationError('Неверный формат файла')
    try:
        if wave.open(value).getparams()[:3] != (1, 2, 8000):
            raise ValidationError('Неверные параметры файла')

    except Exception as e:
        logger.warning(e)
        raise ValidationError('Неверные параметры файла')


class WAVFile(models.Model):
    file = models.FileField(upload_to='.', validators=[validate_wav])
    number = models.CharField(verbose_name='DID номер', max_length=50)
    active = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super(WAVFile, self).__init__(*args, **kwargs)
        self.old_file = self.file.name

    @property
    def filename(self):
        return os.path.basename(self.file.name)


@receiver(post_save, sender=WAVFile)
def save(instance, created, **kwargs):
    build_config(WAVFile.objects.filter(active=True))

    if created:
        return

    if instance.old_file != instance.file.name and os.path.exists(instance.file.path):
        os.remove(instance.file.path)


@receiver(post_delete, sender=WAVFile)
def delete(instance, **kwargs):
    build_config(WAVFile.objects.filter(active=True))
    if os.path.exists(instance.file.path):
        os.remove(instance.file.path)

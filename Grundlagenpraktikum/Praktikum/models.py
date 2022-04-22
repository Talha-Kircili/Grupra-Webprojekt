from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.conf import settings
from django.db import models


''' löscht alte PDF '''
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

@receiver(pre_save)
def delete_files_when_file_changed(sender,instance, **kwargs):
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return
            instance_in_db_file_field = getattr(instance_in_db,field.name)
            instance_file_field = getattr(instance,field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

Wochentage = (
    ('Monday', 'Montag'),
    ('Tuesday', 'Dienstag'),
    ('Wednesday', 'Mittwoch'),
    ('Thursday', 'Donnerstag'),
    ('Friday', 'Freitag')
)

class Wochentag(models.Model):
    day = models.CharField(max_length=10, choices=Wochentage)
    time = models.TimeField()
    def __str__(self):
        return self.day
    class Meta:
        verbose_name_plural = "Wochentage"

class CustomUser(AbstractUser):
    pass
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "Benutzer"

class Versuch(models.Model):
    title = models.TextField(unique=True)
    status = models.BooleanField(default = False)
    document = models.FileField(upload_to = 'pdf/', blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Versuche"

class Aufgabe(models.Model):
    description = models.TextField()
    versuch = models.ForeignKey(Versuch, on_delete=models.CASCADE)
    def __str__(self):
        return self.description
    class Meta:
        verbose_name_plural = "Aufgaben"

def jsonfield_default():
    return []

class Fortschritt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username', limit_choices_to={'is_staff': False}, on_delete=models.CASCADE)
    progress = models.JSONField(default=jsonfield_default)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = "Fortschritte"

class Hilfesuche(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='username', limit_choices_to={'is_staff': False}, on_delete=models.CASCADE)
    priority = models.SmallIntegerField()
    creation_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = "Hilfesuchen"

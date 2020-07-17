from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = ProcessedImageField(processors=[ResizeToFill(250, 150)],
                                format='JPEG', options={'quality': 60}, verbose_name='Фото')
    about_me = models.TextField(verbose_name='Обо мне', blank=True)
    birth_date = models.DateField(blank=True, verbose_name='Дата рождения', default=date.today)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'
        ordering = ['-birth_date']


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)

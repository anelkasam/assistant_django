import jwt
from time import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from assistant.settings import SECRET_KEY


class Family(models.Model):
    """
    Users can belong to the family.
    In the budget part off project all transactions connects by family.
    """
    last_name = models.CharField(max_length=30, verbose_name='Last name')

    def generate_token(self):
        exp = time() + 3600
        return jwt.encode({'family_id': self.id, 'exp': exp},
                          SECRET_KEY, algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['family_id']
            return Family.objects.get(pk=id)
        except:
            pass

    def __str__(self):
        return f'Family {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profile_photos', blank=True, null=True, verbose_name='Profile photo')

    def __str__(self):
        return f'User {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

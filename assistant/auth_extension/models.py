from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Family(models.Model):
    """
    Users can belong to the family.
    In the budget part off project all transactions connects by family.
    """
    last_name = models.CharField(max_length=30, verbose_name='Last name')

    def __str__(self):
        return f'Family {self.last_name}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        return f'User {self.user.username}'


from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
# Event Model
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    date = models.DateField()
    time = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=250)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        default=1,
        related_name='events'
    )
    # participant = models.ManyToManyField(User, related_name='rsvp_events', blank=True)
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_events', blank=True)
    # reverse relation name "rsvp_events"
    asset = models.ImageField(upload_to='events_asset', blank=True, null=True, default='events_asset/default_img.png')

    def __str__(self):
        return self.name
# Participant Model
# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=200)
#     participant_to = models.ManyToManyField(
#         Event,
#         related_name='participants'
#     )

#     def __str__(self):
#         return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200,default="General")
    descriptions = models.CharField(max_length=250)
    #reverse relation name "events"
    def __str__(self):
        return self.name





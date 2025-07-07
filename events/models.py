from django.db import models

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
    # reverse relation name "participants"
    def __str__(self):
        return self.name
# Participant Model
class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    participant_to = models.ManyToManyField(
        Event,
        related_name='participants'
    )

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200,default="General")
    descriptions = models.CharField(max_length=250)
    #reverse relation name "events"
    def __str__(self):
        return self.name





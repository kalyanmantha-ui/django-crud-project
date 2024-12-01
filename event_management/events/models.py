# models.py
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )  # Allow null and blank temporarily
    time = models.TimeField(null=True, blank=True)  # Optional
    location = models.CharField(max_length=200, null=True, blank=True)  # Optional

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

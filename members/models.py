from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    MEMBERSHIP_CHOICES = [
        ('community', 'Community'),
        ('key-access', 'Key Access'),
        ('creative-workspace', 'Creative Workspace'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_CHOICES)  # Add dropdown choices
    password = models.CharField(max_length=100)  # Use hashing later for security

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OngoingEvent(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title

from django.db import models

class Member(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    membership_type = models.CharField(
        max_length=50,
        choices=[('Community', 'Community'), ('Key Access', 'Key Access'), ('Creative Workspace', 'Creative Workspace')]
    )
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    password = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)  # Ensure this field exists

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.db import models

class Event(models.Model):  
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    event_date = models.DateField()
    event_time = models.TimeField()

    def __str__(self):
        return self.name

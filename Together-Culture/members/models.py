from django.db import models

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

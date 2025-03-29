from django.db import models

# Create your models here.
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"Review for {self.event.name}"

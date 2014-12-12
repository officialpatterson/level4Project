from django.db import models
from django.contrib.auth.models import User

class TrackedEntities(models.Model):
    follower = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    notification = models.BooleanField(default=True)
class Notifications(models.Model):
    user = models.ForeignKey(User)
    entity = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
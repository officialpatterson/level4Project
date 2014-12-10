from django.db import models
from django.contrib.auth.models import User

class TrackedEntities(models.Model):
    follower = models.ForeignKey(User)
    name = models.CharField(max_length=100)
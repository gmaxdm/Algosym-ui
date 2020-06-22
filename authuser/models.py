from django.db import models
from django.contrib.auth.models import User


class Logins(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    permit = models.CharField(max_length=100)

    class Meta:
        db_table = "bhacklogins"


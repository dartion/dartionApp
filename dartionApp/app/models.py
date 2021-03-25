from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserAuthKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    auth_key = models.CharField(max_length=100, null=True, blank=True)
    reset_password_key = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(UserAuthKey, self).save(*args, **kwargs)

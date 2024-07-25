from django.db import models
from django.contrib.auth.models import User

class Drops(models.Model):
    key_instance = models.CharField(max_length=100)
    country = models.CharField(max_length=20, blank=True, null=True)
    bot_id = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            if Drops.objects.filter(user=self.user).count() >= 1:
                raise ValueError("Free tier can only have 1 drops")
            super(Drops, self).save(*args, **kwargs)

    def __str__(self):
        return self.key_instance
    
    class Meta:
        verbose_name_plural = "Drops"
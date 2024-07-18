from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

class ImageUser(models.Model):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(pre_save, sender=ImageUser)
def delete_old_profile_images(sender, instance, **kwargs):
    # Verificar si existe una imagen anterior para el mismo usuario
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        
        # Borrar la imagen anterior si es diferente a la nueva
        if old_instance.profile_image and old_instance.profile_image != instance.profile_image:
            old_instance.profile_image.delete(save=False)

    # También eliminar otras imágenes anteriores para el mismo usuario
    previous_images = sender.objects.filter(user=instance.user).exclude(pk=instance.pk)
    for image in previous_images:
        if image.profile_image:
            image.profile_image.delete(save=False)
        image.delete()

@receiver(post_delete, sender=ImageUser)
def delete_profile_image_on_delete(sender, instance, **kwargs):
    if instance.profile_image:
        instance.profile_image.delete(save=False)
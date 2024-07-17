from django.forms import ModelForm
from .models import ImageUser

class ImageUserform(ModelForm):
    class Meta:
        model = ImageUser
        fields = ["profile_image"]

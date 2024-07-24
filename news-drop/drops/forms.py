from django.forms import ModelForm
from .models import Drops

class DropForm(ModelForm):
    class Meta:
        model = Drops
        fields = ["key_instance", "country"]

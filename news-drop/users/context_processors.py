from .models import ImageUser

def profile_image(request):
    if request.user.is_authenticated:
        try:
            image = ImageUser.objects.get(user=request.user)
            return {'profile_image_url': image.profile_image.url}
        except ImageUser.DoesNotExist:
            return {'profile_image_url': None}
    return {'profile_image_url': None}

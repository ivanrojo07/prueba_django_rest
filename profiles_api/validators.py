from django.core.exceptions import ValidationError
from .models import UserProfile

def validate_username(username):
    if UserProfile.objects.filter(**{'{}__iexact'.format(UserProfile.USERNAME_FIELD):username}).exists():
        raise ValidationError('User with this {} already exists'.format(UserProfile.USERNAME_FIELD))
    return username

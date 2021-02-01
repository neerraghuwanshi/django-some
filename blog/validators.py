import os

from django.core.exceptions import ValidationError


def validate_media(file):
    valid_file_extensions = ['.mp4', '.mov', '.3gp', '.png', '.jpg', '.jpeg']
    ext = os.path.splitext(file.name)[1]

    if ext.lower() not in valid_file_extensions:
        raise ValidationError('Media should only be of mp4, 3gp, mov, png, jpg or jpeg extension')
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

genre_choices = [
    ('rock', 'Rock'),
    ('pop', 'Pop'),
    ('hip_hop', 'Hip Hop'),

]


class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(choices=genre_choices, max_length=30)
    file_upload = models.FileField(upload_to='media/music/',
                                   validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Music, related_name='folders')
    genre = models.CharField(choices=genre_choices, max_length=30)
    is_favorites = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='favorite_tracks')
    tracks = models.ManyToManyField(Music, related_name='favorited_by')

    def __str__(self):
        return f'Favorites for {self.user.username}'

from django.contrib import admin
from .models import Music,Folder,Favorite
# Register your models here.
admin.site.register(Music),
admin.site.register(Folder),
admin.site.register(Favorite),
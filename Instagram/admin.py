from django.contrib import admin

# Register your models here.
from Instagram.models import Image, Comment, Like, Follow

admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
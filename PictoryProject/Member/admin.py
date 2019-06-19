from django.contrib import admin
from Member.models import Profile,Following,Follower

# Register your models here.
admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(Following)
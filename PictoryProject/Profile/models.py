from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    #myimage = models.ImageField
    myid = models.ForeignKey(settings.AUTH_USER_MODEL)
    myname = models.CharField(max_length=30,default=False)
    myemail = models.CharField(max_length=30,default=False)
    #mysex = (('Man','Male'),('Woman', 'Female'),)
    introduction = models.CharField(max_length=200,default=False)
    phonenum = models.CharField(max_length=30,default='000-000-000')
    leavebool = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.profile_text
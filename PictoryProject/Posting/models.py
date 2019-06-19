from django.db import models
from django.contrib.auth.models import User
from Member.models import Profile

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    pub_date=models.DateTimeField('ch add date')
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=500)
    like=models.IntegerField(default=0)
    TMP=models.IntegerField(default=0)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,blank =True, null=True)  #포스트를 Profile와 연결

    def __str__(self):     
        return self.title


class Comment(models.Model):
    body = models.TextField(max_length = 100, blank = False)
    cub_date=models.DateTimeField('ch add date')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)  #comment를 포스트랑 연결

    def __str__(self):
        return self.body
    """
    class Meta:
        ordering = ['cub_date'] #정렬 -면 반대
        """


class Report(models.Model):
    title = models.CharField(max_length=100,blank = False)
    content = models.TextField(max_length = 255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null = True)
    rub_date = models.DateTimeField('ch add date')

    class Meta:
        ordering = ['rub_date'] #정렬 -면 반대
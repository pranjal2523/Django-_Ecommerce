from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=264)

    def __str__(self) -> str:
        return self.name

class Article(models.Model):
    title =  models.CharField(max_length=264, blank=False, null= False)
    description =  models.CharField(max_length=264)
    body =  models.CharField(max_length=264)
    tagList= models.ManyToManyField('Tag', blank=True)
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
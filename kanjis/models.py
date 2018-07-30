from django.db import models

from profiles.models import Profile

# Create your models here.


class KanjiItem(models.Model):
	character = models.CharField(max_length=5)
	meaning = models.CharField(max_length=30)
	number = models.IntegerField()


class KanjiExample(models.Model):
	item = models.ForeignKey(KanjiItem, on_delete=models.CASCADE)
	text = models.CharField(max_length=100)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

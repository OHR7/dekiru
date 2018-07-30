from django.db import models

from profiles.models import Profile

# Create your models here.


class KanjiItem(models.Model):
	character = models.CharField(max_length=5)
	meaning = models.CharField(max_length=30)
	number = models.IntegerField()

	def __str__(self):
		return '{} {}'.format(self.id, self.character)


class KanjiExample(models.Model):
	item = models.ForeignKey(KanjiItem, on_delete=models.CASCADE)
	text = models.CharField(max_length=100)
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	favorites = models.ManyToManyField(Profile, blank=True, related_name='favorite_examples')

	def __str__(self):
		return '{} {} {} {}'.format(self.id, self.profile, self.item, self.text)

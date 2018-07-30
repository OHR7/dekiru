from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# TODO add image field

	def __str__(self):
		return '{} {}'.format(self.id, self.user.username)
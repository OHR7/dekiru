from django.contrib.auth.models import User
from django.test import TestCase

from kanjis.models import KanjiItem

# Create your tests here.
from profiles.models import Profile



class KanjiItemViewTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		# Create user
		user_1 = User.objects.create_user(username='testuser1', password='12345')
		user_1.save()
		profile_1 = Profile.objects.create(user=user_1)
		profile_1.save()

		# Create 1 Kanji item
		number_of_kanjis = 10
		kanji_1 = KanjiItem.objects.create(character= '木', meaning='Tree', number=1)
		kanji_1.save()

	def test_view_url_exists_at_desired_location(self):
		login = self.client.login(username='testuser1', password='12345')
		resp = self.client.get('/kanjis/1/')

		# Check our user is logged in
		self.assertEqual(str(resp.context['user']), 'testuser1')
		# Check that we get a 200(OK) response
		self.assertEqual(resp.status_code, 200)
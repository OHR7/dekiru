from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from kanjis.models import KanjiItem, KanjiExample
from pages.views import ItemView, FavoriteExampleToggle
from profiles.models import Profile

# Create your tests here.


class TestItemView(TestCase):
	def setUp(self):
		# Setup
		# Every test needs access to the request factory.
		self.rf = RequestFactory()

		self.user_1 = User.objects.create_user(username='ohr7', password='1234')
		self.user_1.save()

	def test_response_ok(self):
		kanji_1 = KanjiItem.objects.create(character='木', meaning='Tree', number=1)
		kanji_1.save()

		request = self.rf.get('/pages/')
		request.user = self.user_1

		response = ItemView.as_view(
			template_name='home.html',
			object_model=KanjiItem,
			examples_model=KanjiExample,
		)(request, pk=1)
		self.assertEqual(response.status_code, 200)

	def test_empty_pages(self):
		kanji_1 = KanjiItem.objects.create(character='木', meaning='Tree', number=1)
		kanji_1.save()
		pages = [
			('page', '20'),
			('bests_page', '20')
		]

		request = self.rf.get('/pages/1', pages)
		request.user = self.user_1

		response = ItemView.as_view(
			template_name='home.html',
			object_model=KanjiItem,
			examples_model=KanjiExample,
		)(request, pk=1)

		self.assertEqual(response.status_code, 200)

	def test_object_doesnt_exist(self):
		request = self.rf.get('/pages/1')
		request.user = self.user_1

		response = ItemView.as_view(
			template_name='home.html',
			object_model=KanjiItem,
			examples_model=KanjiExample,
		)(request, pk=1)

		self.assertEqual(response.status_code, 302)


class TestFavoriteExampleToggle(TestCase):

	def setUp(self):
		self.rf = RequestFactory()

		self.user_1 = User.objects.create_user(username='ohr7', password='1234')
		self.user_1.save()

		self.profile_1 = Profile.objects.create(user=self.user_1)
		self.profile_1.save()

		self.kanji_1 = KanjiItem.objects.create(character='木', meaning='Tree', number=1)
		self.kanji_1.save()

	def test_view_toggle_if_not_exist(self):
		kanji_example_1 = KanjiExample.objects.create(
			item=self.kanji_1,
			text="Kanji example 1",
			profile=self.profile_1,
		)
		kanji_example_1.save()

		data = {'example_id': '1'}
		# Option to make AJAX Request HTTP_X_REQUESTED_WITH='XMLHttpRequest'
		request = self.rf.post('/pages/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		request.user = self.user_1

		response = FavoriteExampleToggle.as_view(
			example_model=KanjiExample,
		)(request)

		self.assertEqual(response.status_code, 200)

	def test_view_toggle_if_exist(self):
		kanji_example_1 = KanjiExample.objects.create(
			item=self.kanji_1,
			text="Kanji example 1",
			profile=self.profile_1,
		)
		kanji_example_1.favorites.add(self.profile_1)
		kanji_example_1.save()

		data = {'example_id': '1'}
		# Option to make AJAX Request HTTP_X_REQUESTED_WITH='XMLHttpRequest'
		request = self.rf.post('/pages/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		request.user = self.user_1

		response = FavoriteExampleToggle.as_view(
			example_model=KanjiExample,
		)(request)

		self.assertEqual(response.status_code, 200)
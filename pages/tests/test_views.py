from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator
from django.test import TestCase, RequestFactory
from django.urls import reverse

from kanjis.models import KanjiItem, KanjiExample
from pages.views import ItemView


# Create your tests here.


class ItemViewTest(TestCase):
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

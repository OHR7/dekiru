from django.http import HttpResponse

from kanjis.models import KanjiItem, KanjiExample
from pages.views import ItemView, FavoriteExampleToggle, CreateExample

# Create your views here.


class KanjiView(ItemView):
	template_name = 'kanjis/kanji-view.html'
	object_model = KanjiItem
	examples_model = KanjiExample
	item_type = 'kanji'


class FavoriteKanjiExampleToggle(FavoriteExampleToggle):
	example_model = KanjiExample


class CreateKanjiExample(CreateExample):
	example_model = KanjiExample

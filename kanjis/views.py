from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from kanjis.models import KanjiItem, KanjiExample
from pages.views import ItemView, FavoriteExampleToggle, CreateExample

# Create your views here.

# List of decorators to be applied to KanjiView class
decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class KanjiView(ItemView):
	template_name = 'kanjis/kanji-view.html'
	object_model = KanjiItem
	examples_model = KanjiExample
	item_type = 'kanji'


class FavoriteKanjiExampleToggle(FavoriteExampleToggle):
	example_model = KanjiExample


class CreateKanjiExample(CreateExample):
	example_model = KanjiExample

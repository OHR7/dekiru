from django.http import HttpResponse

from kanjis.models import KanjiItem, KanjiExample
from pages.views import ItemView


# Create your views here.


class KanjiView(ItemView):
	template_name = 'kanjis/kanji-view.html'
	object_model = KanjiItem
	examples_model = KanjiExample


def create_example(request):
	if request.is_ajax():
		text = request.POST['text']
		kanji_id = request.POST['kanji']
		# print(text)
		# print(kanji)

		kanji = KanjiExample(
			text=text,
			profile_id=request.user.profile.id,
			kanji_id=kanji_id
		)
		kanji.save()

		return  HttpResponse('')




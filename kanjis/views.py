from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from kanjis.models import KanjiItem, KanjiExample
from pages.views import ItemView

# Create your views here.


class KanjiView(ItemView):
	template_name = 'kanjis/kanji-view.html'
	object_model = KanjiItem
	examples_model = KanjiExample


def favorite_example_toggle(request):
	user = request.user
	if request.is_ajax():
		if user.is_authenticated:
			kanji_example_id = request.POST['kanji_example_id']
			kanji = get_object_or_404(KanjiExample, id=kanji_example_id)
			if user.profile in kanji.favorites.all():
				kanji.favorites.remove(user.profile)
			else:
				kanji.favorites.add(user.profile)
			return HttpResponse('')
			# TODO add response to send the state of the like for rendering purposes


def create_example(request):
	if request.is_ajax():
		text = request.POST['text']
		kanji_id = request.POST['kanji']
		kanji = KanjiExample(
			text=text,
			profile_id=request.user.profile.id,
			kanji_id=kanji_id
		)
		kanji.save()

		return HttpResponse('')

# pages/views.py
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from kanjis.models import KanjiExample, KanjiItem

# Create your views here.


item_model_mapper = {
	'kanji': KanjiItem
}

example_model_mapper = {
	'kanji': KanjiExample
}

class HomePageView(TemplateView):
	template_name = 'home.html'


class ItemView(View):
	"""
	This is a Parent view for the 3 types of items(Kanji, Grammar and Vocabulary)
	Views,
	"""
	template_name = None
	object_model = None
	examples_model = None
	item_type = None

	def dispatch(self, request, *args, **kwargs):
		self.item = self.get_item()
		self.examples = self.get_examples()
		self.best_examples = self.get_best_examples()
		self.my_comment = self.get_my_comment()

		self.init_all_paginator()
		self.init_best_paginator()

		return super().dispatch(request, *args, **kwargs)

	def init_all_paginator(self):
		paginator = Paginator(self.examples, 5)
		page = self.request.GET.get('page')
		try:
			self.examples_page = paginator.page(page)
		except PageNotAnInteger:
			self.examples_page = paginator.page(1)
		except EmptyPage:
			self.examples_page = paginator.page(paginator.num_pages)

	def init_best_paginator(self):
		paginator = Paginator(self.best_examples, 3)
		page = self.request.GET.get('bests_page')
		try:
			self.best_examples_page = paginator.page(page)
		except PageNotAnInteger:
			self.best_examples_page = paginator.page(1)
		except EmptyPage:
			self.best_examples_page = paginator.page(paginator.num_pages)

	def get_item(self):
		pk = self.kwargs.get('pk')
		obj = self.object_model.objects.get(pk=pk)
		return obj

	def get_my_comment(self):
		try:
			comment = self.examples_model.objects.get(profile=self.request.user.profile, item=self.item)
		except MultipleObjectsReturned as e:
			comment = self.examples_model.objects.filter(profile=self.request.user.profile, item=self.item).first()
		except ObjectDoesNotExist as e:
			comment = None
		return comment

	def get_examples(self):
		examples = self.examples_model.objects.filter(item=self.item)
		# Paginator need a queryset ordered
		examples = examples.order_by('id')
		return examples

	def get_context_data(self, **kwargs):
		"""Get the queryset's for object and examples lists and added it to context"""
		context = {
			'object': self.item,
			'examples': self.examples_page,
			'item_type': self.item_type,
			'best_examples': self.best_examples_page,
			'my_comment': self.my_comment,
		}
		context.update(kwargs)
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

	def get_best_examples(self):
		examples = self.examples_model.objects.filter(item=self.item)
		examples = examples.filter(favorites__isnull=False)
		# Paginator need a queryset ordered
		examples = examples.order_by('favorites')
		return examples


class FavoriteExampleToggle(View):
	example_model = None

	def post(self, request, *args, **kwargs):
		user = request.user
		example_id = request.POST.get('example_id')
		if request.is_ajax():
			if user.is_authenticated:
				example = get_object_or_404(self.example_model, id=example_id)
				if user.profile in example.favorites.all():
					example.favorites.remove(user.profile)
				else:
					example.favorites.add(user.profile)
				return HttpResponse('')
		# TODO add response to send the state of the like for rendering purposes


class CreateExample(View):
	example_model = None

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			text = request.POST['text']
			item_id = request.POST['item_id']
			example = self.example_model(
				text=text,
				profile_id=request.user.profile.id,
				item_id=item_id
			)
			example.save()

			return HttpResponse('')
	# TODO limit the profiles to only comment once

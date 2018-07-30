# pages/views.py
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

# Create your views here.


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

	def dispatch(self, request, *args, **kwargs):
		self.item = self.get_item()
		self.examples = self.get_examples()
		self.my_comment = self.get_my_comment()
		paginator = Paginator(self.examples, 2)
		page = self.request.GET.get('page')
		try:
			self.examples_page = paginator.page(page)
		except PageNotAnInteger:
			self.examples_page = paginator.page(1)
		except EmptyPage:
			self.examples_page = paginator.page(paginator.num_pages)
		return super().dispatch(request, *args, **kwargs)

	def get_item(self):
		pk = self.kwargs.get('pk')
		obj = self.object_model.objects.get(pk=pk)
		return obj

	def get_my_comment(self):
		try:
			comment = self.examples_model.objects.get(profile=self.request.user.profile, item=self.item)
		except MultipleObjectsReturned as e:
			comment = self.examples_model.objects.filter(profile=self.request.user.profile, item=self.item).first()
		return comment

	def get_examples(self):
		examples = self.examples_model.objects.filter(item=self.item)
		# Paginator need a queryset ordered
		examples = examples.order_by('id')
		return examples

	def get_context_data(self, **kwargs):
		"""Get the queryset's for object and examples lists and added it to context"""
		context = {'object': self.item, 'examples': self.examples_page, 'my_comment': self.my_comment}
		context.update(kwargs)
		return context

	def get(self, request, *args, **kwargs):
		context = self.get_context_data()
		return render(request, self.template_name, context)

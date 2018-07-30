# pages/views.py
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

	def configure(self):
		self.object = self.get_object()
		self.examples = self.get_examples()
		paginator = Paginator(self.examples, 2)
		page = self.request.GET.get('page1')
		try:
			self.examples_page = paginator.page(page)
		except PageNotAnInteger:
			self.examples_page = paginator.page(1)
		except EmptyPage:
			self.examples_page = paginator.page(paginator.num_pages)

	def get_object(self):
		pk = self.kwargs.get('pk')
		obj = self.object_model.objects.get(pk=pk)
		return obj

	def get_examples(self):
		examples = self.examples_model.objects.filter(item=self.object)
		# Paginator need a queryset ordered
		examples = examples.order_by('id')
		return examples

	def get_context_data(self, **kwargs):
		"""Get the queryset's for object and examples lists and added it to context"""
		context = {'object': self.object, 'examples': self.examples_page}
		context.update(kwargs)
		return context

	def get(self, request, *args, **kwargs):
		self.configure()
		context = self.get_context_data()
		return render(request, self.template_name, context)

# kanjis/urls.py
from django.urls import path
from . import views


urlpatterns = [
	path('<int:pk>/', views.KanjiView.as_view(), name='kanji-view'),

	# Ajax Views
	path('add-example/', views.create_example, name='add-example'),
	path('favorite-example-toggle/', views.favorite_example_toggle, name='favorite-example-toggle'),
]
# kanjis/urls.py
from django.urls import path
from . import views


urlpatterns = [
	path('<int:pk>/', views.KanjiView.as_view(), name='kanji-view'),

	# Ajax Views
	path('add-example/', views.CreateKanjiExample.as_view(), name='add-kanji-example'),
	path('favorite-example-toggle/', views.FavoriteKanjiExampleToggle.as_view(), name='favorite-kanji-example-toggle'),
]
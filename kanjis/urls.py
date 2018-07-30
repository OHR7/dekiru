# kanjis/urls.py
from django.urls import path
from . import views


urlpatterns = [
	path('<int:pk>/', views.KanjiView.as_view(), name='kanji-view'),
	path('add-example/', views.create_example, name='add-example')
]
from django import forms

from kanjis.models import KanjiExample


class KanjiExampleForm(forms.Form):
	text = forms.CharField()

	# def clean_ validations go here


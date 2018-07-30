from django.contrib import admin

from kanjis.models import KanjiItem, KanjiExample

# Register your models here.


admin.site.register(KanjiItem)
admin.site.register(KanjiExample)
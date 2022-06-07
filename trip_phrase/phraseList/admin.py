from django.contrib import admin
from phraseList.models import Phrase, Dicty

# Register your models here.


	
class PhraseAdmin(admin.ModelAdmin):
    list_display = ('id','language','content','diff')

class DictyAdmin(admin.ModelAdmin):
    list_display = ('source_language','target_language')

admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Dicty, DictyAdmin)
from django.shortcuts import render, redirect
from phraseList.models import Phrase, Dicty, Language
from django.http import HttpResponse


# Create your views here.

def select_language (request):
    languages = [f[1] for f in Language.choices]
    return render(request, 'phraseList/select_language.html', { 'languages' : languages })

def french_home(request): 

    phrases = Phrase.objects.all().filter(language = 'FR')
    return render(request, 'phraseList/lang_home.html',{'phrases' : phrases})
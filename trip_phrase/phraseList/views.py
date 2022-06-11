from django.shortcuts import render, redirect
from phraseList.models import Phrase, Dicty, Language
from django.http import HttpResponse
from phraseList.forms import ChooseContextForm


# Create your views here.

def select_dicty(request):
    dictys = Dicty.objects.all()
    return render(request, 'phraseList/select_dicty.html', { 'dictys': dictys })

def dicty_home(request, id): 
    dicty = Dicty.objects.get(id=id)
    return render(request, 'phraseList/dicty_home.html',{'dicty' : dicty})
    
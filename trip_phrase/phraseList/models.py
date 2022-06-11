from email.policy import default
from multiprocessing import context
from django.db import models

# Create your models here.

class Language(models.TextChoices):
        FRENCH = 'FR'
        ENGLISH = 'EN'
        CROATIAN = 'CR'
        SLOVENIAN = 'SL'

class Context(models.TextChoices):
        TIME = 'time'
        NUMBRES = 'Numbers'
        GENERAL = 'GG'
        DIRECTION = 'Direction'
        RESTAURANT = 'Restaurant_bar'
        SALUTATION = 'Salutation'
        PRESENTATION = 'Presentation'
        REMERCIEMENT = 'Remerciement'


class Phrase(models.Model):
    
    class Diff(models.TextChoices):
        NEW = '1'
        BEG = '2'
        MID = '3'
        FLU = '4'
        EXP = '5'
                
    diff = models.CharField(choices=Diff.choices, max_length=5)
    skill = models.FloatField(blank = True, null = True)
    context = models.CharField(choices=Context.choices, max_length=500, default='GG')
    content = models.CharField(max_length=150)
    language = models.CharField(choices=Language.choices, max_length=5)
    to_learn = models.BooleanField(default = False)
    last_learn = models.DateField(blank = True, null = True)
    traductions = models.ManyToManyField("self", blank = True)
    #synonym =  models.ManyToManyField(Phrase)
    
    @classmethod
    def __str__(self):
        return f'{self.id}'
    
    @classmethod
    def create(cls, language, content, context):
        phrase = cls(language = language, content = content, context = context)
        phrase.save()
        return phrase



class Dicty(models.Model):

    title = models.CharField(max_length=50)
    source_phrases = models.ManyToManyField(Phrase)
    source_language = models.CharField(max_length=5, choices=Language.choices)
    target_language = models.CharField(max_length=5, choices=Language.choices)
    
  
    @property
    def save_link(self, phrase_src,phrase_target):

        phrase_src = Phrase.objects.get(id=phrase_src.id)
        phrase_target = Phrase.objects.get(id=phrase_target.id)

        phrase_src.traductions.add(phrase_target)
        phrase_src.save()

        self.source_phrases.add(phrase_src)
        self.save()

    @property
    def phrase_create(self, language, content, context):
        phrase = Phrase.create(language,content,context)
        return phrase
    
    def read_dicty_directory(self, path):
        import os
        FILE_PATH = path
        context = ''
        source_phrase = ''
        target_phrase = ''
        
        result = dict()
        phraseList = list()
        
        for file in os.listdir(FILE_PATH):
            if file.endswith('.txt'):
                context = file.replace('.txt','')
                with open(f'{FILE_PATH}/{file}') as f:
                    for line in f.readlines():
                        sub = line.split(':')
                        if len(sub)>1:
                            source_phrase = sub[0].lower().replace('\n','').strip()
                            target_phrase = sub[1].lower().replace('\n','').strip()
                            result = {'src_phrase' : source_phrase, 'trg_phrase' : target_phrase, 'context' : context}
                            phraseList.append(result)
        
        return phraseList

   
    def build(self, title, src_lang, target_lang, dicty_rep_path):

        self.title = title
        self.source_language = src_lang
        self.target_language = target_lang

        to_build = self.read_dicty_directory(dicty_rep_path)

        for el in to_build:
            src_phrase = el['src_phrase']
            trg_phrase = el['trg_phrase']
            context = el['context']
            phrase_src = self.phrase_create(src_lang, src_phrase, context)
            phrase_target = self.phrase_create(target_lang,trg_phrase,context)
            self.save_link(phrase_src,phrase_target)

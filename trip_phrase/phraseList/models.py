from email.policy import default
from multiprocessing import context
from django.db import models

# Create your models here.

class Language(models.TextChoices):
        FRENCH = 'FR'
        ENGLISH = 'EN'
        SLOVENIAN = 'SL'
        CROATIAN = 'CR'

class Phrase(models.Model):
    
    class Diff(models.TextChoices):
        NEW = '1'
        BEG= '2'
        MID = '3'
        FLU = '4'
        EXP = '5'

    class Context(models.TextChoices):
        RESTAURANT = 'Restaurant_bar'
        PRESENTATION = 'Presentation'
        SALUTATION = 'Salutation'
        NUMBRES = 'Numbers'
        DIRECTION = 'Direction'
        REMERCIEMENT = 'Remerciement'
        TIME = 'time'
        GENERAL = 'GG'

    language = models.CharField(choices=Language.choices, max_length=5)

    content = models.CharField(max_length=150)
    traductions = models.ManyToManyField("self", blank = True)
    diff = models.CharField(choices=Diff.choices, max_length=5)
    context = models.CharField(choices=Context.choices, max_length=500, default='GG')
    #synonym =  models.ManyToManyField(Phrase)
    to_learn = models.BooleanField(default = False)
    last_learn = models.DateField(blank = True, null = True)
    skill = models.FloatField(blank = True, null = True)

    @classmethod
    def __str__(self):
        return f'{self.id}'
    
    @classmethod
    def create(cls, language, content, context):
        phrase = cls(language = language, content = content, context = context)
        return phrase



class Dicty(models.Model):

    title = models.CharField(max_length=50)
    source_language = models.CharField(max_length=5, choices=Language.choices)
    target_language = models.CharField(max_length=5, choices=Language.choices)
    ## dicty stock les donne sous la forme : {'id_phrase_src' = id_phrase_target, etc}


    def save_link(self, phrase_src,phrase_target):
        phrase_src.traductions.add(phrase_target)

    def phrase_create(self, language, content, context):
        phrase = Phrase.create(language,content,context)
        phrase.save()
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
            phrase_target = self.phrase_create(target_lang,trg_phrase, context)
            self.save_link(phrase_src,phrase_target)


    #def link(src,trg)
        
from email.policy import default
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
        RESTAURANT = 'rt'
        TAXI = 'tx'
        BAR = 'br'
        MEETING = 'rc'

    language = models.CharField(choices=Language.choices, max_length=5)

    content = models.CharField(max_length=150)
    # traductions = models.ManyToManyField(Phrase, blank = True, null = True)

    diff = models.CharField(choices=Diff.choices, max_length=5)
    #context= models.CharField(choices=Context.choices, max_length=500)
    #synonym =  models.ManyToManyField(Phrase)
    to_learn = models.BooleanField(default = False)
    last_learn = models.DateField(blank = True, null = True)
    skill = models.FloatField(blank = True, null = True)

    def __str__(self):
        return f'{self.id}'


class Dicty(models.Model):

    title = models.CharField(max_length=50)
    source_language = models.CharField(max_length=5, choices=Language.choices)
    target_language = models.CharField(max_length=5, choices=Language.choices)
    dicty = models.JSONField(default = '')

    def phrase_create(self, language, content): #
        pass

    def dicty_build(self, phrase_src, phrase_trg):
        pass

    def read_dicty_file(self, file_name):
        filename = file_name

        source_list = []
        target_list = []
        source_phrase = ''
        target_phrase = ''
        line = ''
        with open(filename) as f:
            line = f.readline()
            sub = line.split(pattern = ':',maxsplit=1)
            source_phrase = sub[0]
            target_phrase = sub[1]
        pass
from django.contrib.auth.models import User
from django.db import models

class Aktyor(models.Model):
    TANLOV = (
        ('Erkak','Erkak'),
        ('Ayol','Ayol')
    )
    DAVLATLAR = (
        ('Uzbekistan', 'Uzbekistan'),
        ('Russia', 'Russia'),
        ('Armenia', 'Armenia'),
        ('Tajikistan', 'Tajikistan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kyrgzstan', 'Kyrgzstan'),
        ('Azerbayjan', 'Azerbayjan'),
        ('Moldova', 'Moldova'),
        ('Latviya', 'Latviya'),
        ('Turkmenistan', 'Turkmenistan'),
    )
    ism = models.CharField(max_length=30)
    sharif = models.CharField(max_length=30)
    davlat = models.CharField(max_length=50,choices=DAVLATLAR)
    tugilgan_yil = models.DateField()
    jins = models.CharField(max_length=40,choices=TANLOV)



class Kino(models.Model):
    nom = models.CharField(max_length=50)
    janr = models.CharField(max_length=40)
    yil = models.DateField()
    davomiylik = models.DurationField()
    aktyorlar = models.ManyToManyField(Aktyor)
    reyting = models.FloatField(default=0)



class Izoh(models.Model):
    matn = models.CharField(max_length=150,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sana = models.DateField(auto_now=True)
    baho = models.FloatField()
    kino = models.ForeignKey(Kino, on_delete=models.CASCADE)



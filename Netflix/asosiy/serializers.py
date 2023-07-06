from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .models import Aktyor, Kino, Izoh


class AktyorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ism = serializers.CharField(max_length=30)
    sharif = serializers.CharField(max_length=30)
    davlat = serializers.CharField(max_length=50)
    tugilgan_yil = serializers.DateField()
    jins = serializers.CharField(max_length=40)

    def validate_ism(self,qiymat):
        if len(qiymat) < 3:
            raise serializers.ValidationError("ism bunaqa kalta bolishi mumkin emas")
        return qiymat


# class KinoSerializer(serializers.ModelSerializer):
#     aktyorlar = AktyorSerializer(many=True,read_only=True)
#     class Meta:
#         model = Kino
#         fields = '__all__'

class AktyorlarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aktyor
        fields = '__all__'

class KinoSerializer(serializers.ModelSerializer):
    aktyorlar = AktyorlarSerializer(many=True)
    class Meta:
        model = Kino
        fields = '__all__'

class KinoSaqlaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class IzohlarSerializer(serializers.ModelSerializer):
    kino = KinoSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Izoh
        fields = '__all__'


class IzohSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Izoh
        fields = '__all__'

    def validate_baho(self,malumot):
        if malumot < 0:
            raise serializers.ValidationError("Kichikroq son yozing")
        elif malumot > 6:
            raise serializers.ValidationError("Kattaroq son yozing")
        return malumot



    def validate_matn(self,matn):
        tanlov = ['Yomon','Ortacha','Oxshamapti']
        if matn in tanlov:
            raise serializers.ValidationError("Mumkin emas bunday yozish")
        return matn

# class IzohSerializer(serializers.Serializer):





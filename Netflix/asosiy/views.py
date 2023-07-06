from django.shortcuts import render,redirect
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from django.contrib.postgres.search import TrigramSimilarity




class HelloView(APIView):
    def get(self,request):
        d = {
            "xabar":"Salom Dunyo",
            "vaqt":"2023-06-22"
        }
        return Response(d)

    def post(self,request):
        malumot = request.data
        d = {
            "xabar": "post qabul qilindi",
            "post_malumoti": malumot
        }
        return Response(d)

class AktyorlarAPIView(APIView):
    def get(self,request):
        soz = request.query_params.get('qidiruv')
        if soz:
            aktyorlar = Aktyor.objects.annotate(
                oxshashlik = TrigramSimilarity('ism',soz)
            ).filter(oxshashlik__gte=0.4)
            print(aktyorlar)
        else:
            aktyorlar = Aktyor.objects.all()
        serializer = AktyorSerializer(aktyorlar,many=True)
        return Response(serializer.data)

    def post(self,request):
        malumot = request.data
        serializer = AktyorSerializer(data=malumot)
        if serializer.is_valid():
            Aktyor.objects.create(
                ism = serializer.validated_data.get('ism'),
                sharif = serializer.validated_data.get('sharif'),
                davlat = serializer.validated_data.get('davlat'),
                tugilgan_yil = serializer.validated_data.get('tugilgan_yil'),
                jins = serializer.validated_data.get('jins'),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AktyorDetail(APIView):
    def delete(self,request,pk):
        Aktyor.objects.get(id=pk).delete()
        return Response(status=status.HTTP_100_CONTINUE)



# class AktyorAPIView(APIView):
#     def get(self,request,pk):
#         aktyor = Aktyor.objects.get(id=pk)
#         serializer = AktyorSerializer(aktyor)
#         return Response(serializer.data)


class IzohlarAPIView(APIView):
    def get(self,request):
        izohlar = Izoh.objects.all()
        serializer = IzohlarSerializer(izohlar,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        izoh = request.data
        serializer = IzohSaveSerializer(data=izoh)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IzohDetail(APIView):
    def get(self,request,pk):
        izoh = Izoh.objects.get(id=pk)
        serializer = IzohlarSerializer(izoh)
        return Response(serializer.data,status=status.HTTP_200_OK)


class KinolarAPIView(APIView):
    def get(self,request):
        soz = request.query_params.get('qidiruv')
        if soz:
            kino = Kino.objects.filter(nom__icontains=soz)
        else:
            kino = Kino.objects.all()
        serializer = KinoSerializer(kino, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self,request):
        kino = request.data
        serializer = KinoSaqlaSerializer(data=kino)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class KinoView(APIView):
#     def get(self,request,pk):
#         kino = Kino.objects.get(id=pk)
#         serializer = KinoSerializer(kino)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#
#     def delete(self,request,pk):
#         Kino.objects.get(id=pk).delete()
#         malumot = {
#             "xabar":"Kino ma'lumoti ochirildi"
#         }
#         return Response(malumot,status=status.HTTP_202_ACCEPTED)
#
#
#     def put(self,request,pk):
#         kino = Kino.objects.get(id=pk)
#         malumot = request.data
#         serializer = KinoSaqlaSerializer(kino, data=malumot)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KinoModelViewSet(ModelViewSet):
    queryset = Kino.objects.all()
    serializer_class = KinoSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['nom','janr']
    ordering_fields = ['davomiylik','reyting']

    @action(detail=True,methods=['GET','POST'])
    def aktyorlar(self,request,pk):
        if request.method == 'POST':
            aktyor = request.data
            kino = self.get_object()
            serializer = AktyorSerializer(data=aktyor)
            if serializer.is_valid():
                a = Aktyor.objects.create(
                    ism=serializer.validated_data.get('ism'),
                    davlat=serializer.validated_data.get('davlat'),
                    tugilgan_yil=serializer.validated_data.get('tugilgan_yil'),
                    jins=serializer.validated_data.get('jins'),
                )
                kino.aktyorlar.add(a)
                kino.save()
        kino = self.get_object()
        actors = kino.aktyorlar.all()
        serializer = AktyorSerializer(actors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class AktyorModelViewSet(ModelViewSet):
    queryset = Aktyor.objects.all()
    serializer_class = AktyorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ism','sharif','davlat']
    ordering_fields = ['ism']








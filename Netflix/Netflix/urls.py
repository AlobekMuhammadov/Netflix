from django.contrib import admin
from django.urls import path, include
from asosiy.views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("aktyorlar",AktyorModelViewSet)
router.register("kinolar",KinoModelViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('aktyorlar_api/', AktyorlarAPIView.as_view()),
    path('izohlar/', IzohlarAPIView.as_view()),
    path('kinolar_api/', KinolarAPIView.as_view()),
    # path('kino/<int:pk>/', KinoView.as_view()),
    # path('aktyor/<int:pk>/', AktyorAPIView.as_view()),
]

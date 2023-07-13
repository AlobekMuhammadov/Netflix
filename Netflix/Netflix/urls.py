from django.contrib import admin
from django.urls import path, include
from asosiy.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from drf_spectacular.views import SpectacularSwaggerView, \
    SpectacularRedocView,\
    SpectacularAPIView



router = DefaultRouter()
router.register("aktyorlar",AktyorModelViewSet)
router.register("kinolar",KinoModelViewSet)
router.register("izohlar",IzohModelViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('aktyorlar_api/', AktyorlarAPIView.as_view()),
    path('apiview_docs/', SpectacularAPIView.as_view(),name="schema"),
    path('docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('redoc/', SpectacularRedocView.as_view(url_name="schema")),
    # path('izohlar/', IzohlarAPIView.as_view()),
    path('token_olish/', TokenObtainPairView.as_view()),
    path('token_yangilash/', TokenRefreshView.as_view()),
    path('kinolar_api/', KinolarAPIView.as_view()),
    # path('kino/<int:pk>/', KinoView.as_view()),
    # path('aktyor/<int:pk>/', AktyorAPIView.as_view()),
]

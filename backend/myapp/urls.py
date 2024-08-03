# myapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OOADViewSet, UnidadViewSet, CriterioViewSet, SubCriterioViewSet, 
    AccionViewSet, SeguimientoViewSet, BandaViewSet, SubBandaViewSet, CustomUserViewSet
)

router = DefaultRouter()
router.register(r'ooads', OOADViewSet)
router.register(r'unidades', UnidadViewSet)
router.register(r'criterios', CriterioViewSet)
router.register(r'subcriterios', SubCriterioViewSet)
router.register(r'acciones', AccionViewSet)
router.register(r'seguimientos', SeguimientoViewSet)
router.register(r'bandas', BandaViewSet)
router.register(r'subbandas', SubBandaViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

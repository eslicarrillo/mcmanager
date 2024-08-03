# myapp/views.py

from rest_framework import viewsets
from .models import OOAD, Unidad, Criterio, SubCriterio, Accion, Seguimiento, Banda, SubBanda, CustomUser
from .serializers import (
    OOADSerializer, UnidadSerializer, CriterioSerializer, SubCriterioSerializer, 
    AccionSerializer, SeguimientoSerializer, BandaSerializer, SubBandaSerializer, CustomUserSerializer
)

class OOADViewSet(viewsets.ModelViewSet):
    queryset = OOAD.objects.all()
    serializer_class = OOADSerializer

class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer

class CriterioViewSet(viewsets.ModelViewSet):
    queryset = Criterio.objects.all()
    serializer_class = CriterioSerializer

class SubCriterioViewSet(viewsets.ModelViewSet):
    queryset = SubCriterio.objects.all()
    serializer_class = SubCriterioSerializer

class AccionViewSet(viewsets.ModelViewSet):
    queryset = Accion.objects.all()
    serializer_class = AccionSerializer

class SeguimientoViewSet(viewsets.ModelViewSet):
    queryset = Seguimiento.objects.all()
    serializer_class = SeguimientoSerializer

class BandaViewSet(viewsets.ModelViewSet):
    queryset = Banda.objects.all()
    serializer_class = BandaSerializer

class SubBandaViewSet(viewsets.ModelViewSet):
    queryset = SubBanda.objects.all()
    serializer_class = SubBandaSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

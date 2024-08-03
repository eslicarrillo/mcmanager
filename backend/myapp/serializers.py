# myapp/serializers.py

from rest_framework import serializers
from .models import OOAD, Unidad, Criterio, SubCriterio, Accion, Seguimiento, Banda, SubBanda, CustomUser

class OOADSerializer(serializers.ModelSerializer):
    class Meta:
        model = OOAD
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'

class CriterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterio
        fields = '__all__'

class SubCriterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCriterio
        fields = '__all__'

class AccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accion
        fields = '__all__'

class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = '__all__'

class BandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banda
        fields = '__all__'

class SubBandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBanda
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

from django.db import models
from django.contrib.auth.models import AbstractUser

class OOAD(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Unidad(models.Model):
    name = models.CharField(max_length=100)
    ooad = models.ForeignKey(OOAD, related_name='unidades', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='unidad_photos/', null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
    values = models.TextField(null=True, blank=True)
    politica_calidad = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    personal_confianza = models.IntegerField(null=True, blank=True)
    personal_base = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def calcular_puntaje_total(self):
        total_puntaje = 0
        for criterio in self.criterios.all():
            total_puntaje += criterio.calcular_puntaje()
        return total_puntaje

    def determinar_madurez(self):
        puntaje_total = self.calcular_puntaje_total()
        for banda in Banda.objects.all():
            for sub_banda in banda.subbandas.all():
                if sub_banda.min_puntaje <= puntaje_total <= sub_banda.max_puntaje:
                    return f"{banda.name} - {sub_banda.name}"
        return "No determinado"

class Criterio(models.Model):
    name = models.CharField(max_length=100)
    unidad = models.ForeignKey(Unidad, related_name='criterios', on_delete=models.CASCADE)
    lider = models.ForeignKey('CustomUser', related_name='lider_criterios', on_delete=models.SET_NULL, null=True, blank=True)
    miembros = models.ManyToManyField('CustomUser', related_name='miembro_criterios', blank=True)
    nomenclatura = models.CharField(max_length=10, help_text="Ejemplo: 1")

    def __str__(self):
        return f"{self.nomenclatura} {self.name}"

    def calcular_puntaje(self):
        puntaje = 0
        for subcriterio in self.subcriterios.all():
            puntaje += subcriterio.calcular_puntaje()
        return puntaje

class SubCriterio(models.Model):
    name = models.CharField(max_length=100)
    criterio = models.ForeignKey(Criterio, related_name='subcriterios', on_delete=models.CASCADE)
    nomenclatura = models.CharField(max_length=10, help_text="Ejemplo: 1.1")

    def __str__(self):
        return f"{self.nomenclatura} {self.name}"

    def calcular_puntaje(self):
        puntaje = 0
        for accion in self.acciones.all():
            seguimiento = accion.seguimientos.last()  # Suponiendo que tomamos el último seguimiento
            if seguimiento:
                if seguimiento.status == 'cumple':
                    puntaje += accion.weight_full
                elif seguimiento.status == 'parcial':
                    puntaje += accion.weight_partial
                elif seguimiento.status == 'no_cumple':
                    puntaje += accion.weight_none
        return puntaje

class Accion(models.Model):
    name = models.CharField(max_length=100)
    subcriterio = models.ForeignKey(SubCriterio, related_name='acciones', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    weight_full = models.FloatField(null=True, blank=True)   # Peso cuando se cumple completamente
    weight_partial = models.FloatField(null=True, blank=True)  # Peso cuando se cumple parcialmente
    weight_none = models.FloatField(null=True, blank=True)   # Peso cuando no se cumple

    def __str__(self):
        return self.name

class Seguimiento(models.Model):
    STATUS_CHOICES = [
        ('cumple', 'Cumple'),
        ('parcial', 'Parcial'),
        ('no_cumple', 'No Cumple')
    ]
    accion = models.ForeignKey(Accion, related_name='seguimientos', on_delete=models.CASCADE)
    progress = models.TextField(null=True, blank=True)
    evidence = models.FileField(upload_to='evidences/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"Seguimiento de {self.accion.name}"

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('lider', 'Líder de Criterio'),
        ('miembro', 'Equipo de Criterio'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    can_access_module_a = models.BooleanField(default=False)
    can_access_module_b = models.BooleanField(default=False)
    can_access_module_c = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.assign_permissions_based_on_role()

    def assign_permissions_based_on_role(self):
        if self.role == 'admin':
            self.can_access_module_a = True
            self.can_access_module_b = True
            self.can_access_module_c = True
        elif self.role == 'supervisor':
            self.can_access_module_a = True
            self.can_access_module_b = True
        elif self.role == 'lider':
            self.can_access_module_a = True
        elif self.role == 'miembro':
            self.can_access_module_a = False
            self.can_access_module_b = False
            self.can_access_module_c = False
        self.save()

class Banda(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubBanda(models.Model):
    name = models.CharField(max_length=100)
    banda = models.ForeignKey(Banda, related_name='subbandas', on_delete=models.CASCADE)
    min_puntaje = models.FloatField(null=True, blank=True)
    max_puntaje = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.banda.name} - {self.name}"

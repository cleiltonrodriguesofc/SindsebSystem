from django.contrib import admin
from .models import Socio, SocioDependent, SocioTrabalho, SocioEndereco, Lotacao

# Register your models here.





admin.site.register(Socio)
admin.site.register(SocioEndereco)
admin.site.register(SocioTrabalho)
admin.site.register(Lotacao)
admin.site.register(SocioDependent)

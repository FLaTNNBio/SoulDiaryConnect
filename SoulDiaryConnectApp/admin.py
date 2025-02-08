from django.contrib import admin
from .models import Medico, Paziente, NotaDiario, Messaggio

admin.site.register(Medico)
admin.site.register(Paziente)
admin.site.register(NotaDiario)
admin.site.register(Messaggio)

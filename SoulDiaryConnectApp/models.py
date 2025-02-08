from django.db import models

class Medico(models.Model):
    codice_identificativo = models.CharField(max_length=12, primary_key=True)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    indirizzo_studio = models.CharField(max_length=30)
    citta = models.CharField(max_length=30)
    numero_civico = models.CharField(max_length=6)
    numero_telefono_studio = models.CharField(max_length=13, unique=True, null=True, blank=True)
    numero_telefono_cellulare = models.CharField(max_length=13, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=50)
    tipo_nota = models.BooleanField(null=True, blank=True)
    lunghezza_nota = models.BooleanField(null=True, blank=True)
    tipo_parametri = models.CharField(max_length=400, null=True, blank=True)
    testo_parametri = models.CharField(max_length=2500, null=True, blank=True)

class Paziente(models.Model):
    codice_fiscale = models.CharField(max_length=16, primary_key=True)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    data_di_nascita = models.DateField()
    med = models.ForeignKey(Medico, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=50)

class NotaDiario(models.Model):
    id = models.AutoField(primary_key=True)
    paz = models.ForeignKey(Paziente, on_delete=models.CASCADE)
    testo_paziente = models.TextField()
    testo_supporto = models.TextField(null=True, blank=True)
    testo_clico = models.TextField()
    testo_medico = models.TextField(null=True, blank=True)
    data_nota = models.DateField()

class Messaggio(models.Model):
    id = models.AutoField(primary_key=True)
    med = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paz = models.ForeignKey(Paziente, on_delete=models.CASCADE)
    testo = models.TextField()
    data_messaggio = models.DateField()
    mittente = models.CharField(max_length=12)

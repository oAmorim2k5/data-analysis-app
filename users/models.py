from django.db import models

class AccountRequest(models.Model):
    FULLNAME = models.CharField(max_length=255)
    EMAIL = models.EmailField(unique=True)
    COMPANY_NAME = models.CharField(max_length=255)
    PASSWORD = models.CharField(max_length=255) 
    REQ_DATE = models.DateTimeField(
        auto_now_add=True, # Usa o momento da criação no fuso horário local
        verbose_name="Data de Solicitação"
    )
    STATUS = models.CharField(max_length=10)

    class Meta:
        db_table = 'accountrequest' 
        app_label = 'users' 
        managed = False  
from django.db import models

class Visit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Data e Hora")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Endereço IP")
    page = models.CharField(max_length=100, default="Home", verbose_name="Página Visitada")

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Contador de Visitas"
        ordering = ['-timestamp']

    def __str__(self):
        return f"Acesso em {self.timestamp.strftime('%d/%m/%Y às %H:%M')}"

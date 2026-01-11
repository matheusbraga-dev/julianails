from django.db import models


class BookingConfig(models.Model):
    schedule = models.CharField(
        "Horário", max_length=100, default="Manhã: 07:00 às 12:00"
    )

    class Meta:
        verbose_name = "Configuração de Agendamento"
        verbose_name_plural = "Configurações de Agendamento"
        db_table = 'booking_config'

    def __str__(self):
        return self.schedule

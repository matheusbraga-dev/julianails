from pytest_django.fixtures import db
from django.core.exceptions import ValidationError
from django.db import models
from .base import SingletonModel


class ScheduleConfig(SingletonModel):
    only_current_month = models.BooleanField(
        "Permitir agendamentos apenas no mês atual?",
        default=False,
        help_text="Se marcado, os agendamentos só poderão ser feitos dentro do mês corrente.",
    )

    max_days_ahead = models.PositiveIntegerField(
        "Quantos dias à frente os agendamentos são permitidos?",
        default=30,
        help_text="Usado quando 'Permitir agendamentos apenas no mês atual?' não está marcado.",
    )

    works_sunday = models.BooleanField("Domingo", default=False)
    works_monday = models.BooleanField("Segunda-feira", default=True)
    works_tuesday = models.BooleanField("Terça-feira", default=True)
    works_wednesday = models.BooleanField("Quarta-feira", default=True)
    works_thursday = models.BooleanField("Quinta-feira", default=True)
    works_friday = models.BooleanField("Sexta-feira", default=True)
    works_saturday = models.BooleanField("Sábado", default=True)

    class Meta:
        verbose_name = "Configurações de Agendamento Personalizada"
        verbose_name_plural = "Configurações de Agendamento Personalizadas"
        db_table = 'schedule_config'

    def __str__(self):
        return "Configurações de Agendamento Personalizada"

class BlockedDate(models.Model):
    start_date = models.DateField("Data de início")
    end_date = models.DateField("Data de término")
    reason = models.CharField("Motivo", max_length=100, blank=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Data Bloqueada"
        verbose_name_plural = "Datas Bloqueadas"
        db_table = 'blocked_dates'

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                "Data de término não pode ser anterior à data de início."
            )

    def __str__(self):
        if self.start_date == self.end_date:
            return f"{self.start_date}"
        return f"{self.start_date} → {self.end_date}"

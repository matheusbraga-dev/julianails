from django.db import models
from .base import TimeStampedModel


class Service(TimeStampedModel):
    ICON_CHOICES = [
        ('fa-hand-sparkles', 'Mão com Brilho'),
        ('fa-gem', 'Diamante'),
        ('fa-paint-brush', 'Pincel'),
        ('fa-spa', 'Flor de Lótus'),
        ('fa-seedling', 'Muda de Planta'),
        ('fa-heart', 'Coração'),
        ('fa-star', 'Estrela'),
        ('fa-magic', 'Varinha Mágica'),
    ]

    title = models.CharField("Título", max_length=100)
    description = models.TextField("Descrição", max_length=1000)
    price = models.DecimalField("Preço", max_digits=6, decimal_places=2)
    icon = models.CharField("Ícone", max_length=50, choices=ICON_CHOICES, default='fa-hand-sparkles')
    is_sale = models.BooleanField("Destacar como Promoção?", default=False)
    is_popular = models.BooleanField("Destacar como Popular?", default=False)
    active = models.BooleanField("Ativo", default=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'services'
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.title

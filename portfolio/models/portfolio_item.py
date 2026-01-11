from django.db import models
from .base import TimeStampedModel

class PortfolioItem(TimeStampedModel):
    title = models.CharField("Título", max_length=100, help_text="Texto alt da imagem")
    image = models.ImageField("Imagem", upload_to='portfolio/')

    class Meta:
        ordering = ['-created_at']
        db_table = 'portfolio_items'
        verbose_name = "Item de Portfólio"
        verbose_name_plural = "Itens de Portfólio"

    def __str__(self):
        return self.title


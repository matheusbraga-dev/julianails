from django.db import models
from .base import SingletonModel


class BusinessConfig(SingletonModel):
    """
    Modelo Singleton para armazenar informações globais do site.
    Idealmente, deve haver apenas 1 registro deste modelo.
    """
    site_name = models.CharField("Nome do Site", max_length=100, default="Julia Ellen Nails")
    phone_display = models.CharField("Telefone para Exibição", max_length=20, help_text="Ex: (81) 99999-9999")
    whatsapp_number = models.CharField("Número do WhatsApp", max_length=20, help_text="Apenas números. Ex: 5581999999999")
    instagram_handle = models.CharField("Instagram", max_length=50, help_text="Sem o @. Ex: juliaellen.nails")
    address = models.CharField("Endereço", max_length=200, default="Cosme Damião - Camaragibe")
    
    # Seção Sobre
    about_image = models.ImageField("Imagem Sobre", upload_to='about/', blank=True, null=True)
    about_text_p1 = models.TextField("Sobre - Parágrafo 1")
    about_text_p2 = models.TextField("Sobre - Parágrafo 2", blank=True)
    opening_days = models.CharField("Dias de Funcionamento", max_length=50, default="Segunda a Sábado")
    opening_hours = models.CharField("Horário de Funcionamento", max_length=50, default="07:00 às 18:00")

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configurações do Site"
        db_table = 'business_config'

    def __str__(self):
        return self.site_name

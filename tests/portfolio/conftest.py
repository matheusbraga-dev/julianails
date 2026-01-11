import pytest

from portfolio.models.business_config import BusinessConfig
from portfolio.models.portfolio_item import PortfolioItem
from portfolio.models.service import Service

@pytest.fixture
def business_config(db):
    """Cria e retorna uma instância de configuração do site."""
    return BusinessConfig.objects.create(
        site_name="Julia Ellen Nails",
        phone_display="(81) 99999-9999",
        whatsapp_number="5581999999999",
        instagram_handle="juliaellen.nails",
        address="Cosme Damião - Camaragibe",
        about_image=None,
        about_text_p1="Texto sobre padrão",
        opening_days="Segunda a Sábado",
        opening_hours="07:00 às 18:00",
    )

@pytest.fixture
def service_manicure(db):
    """Cria um serviço padrão."""
    return Service.objects.create(
        title="Manicure Simples",
        description="Cutilagem e esmaltação",
        price=35.00,
        active=True
    )

@pytest.fixture
def portfolio_item(db):
    """Cria um item de portfólio."""
    return PortfolioItem.objects.create(
        title="Unha Gel",
        image="portfolio/teste.jpg"
    )

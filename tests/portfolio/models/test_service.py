import pytest
from portfolio.models.service import Service


@pytest.mark.django_db
def test_service_defaults():
    service = Service.objects.create(
        title="Pedicure",
        description="Apenas teste",
        price=40.00
    )

    assert service.active is True
    assert service.is_sale is False
    assert service.icon == 'fa-hand-sparkles'


@pytest.mark.django_db
def test_service_str_method(service_manicure):
    assert str(service_manicure) == "Manicure Simples"
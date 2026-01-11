import pytest
from portfolio.models.booking_config import BookingConfig


@pytest.mark.django_db
def test_booking_config_default_schedule():
    config = BookingConfig.objects.create()
    assert "Manhã: 07:00 às 12:00" in config.schedule


@pytest.mark.django_db
def test_booking_config_str():
    config = BookingConfig.objects.create(schedule="Tarde Exclusiva")
    assert str(config) == "Tarde Exclusiva"
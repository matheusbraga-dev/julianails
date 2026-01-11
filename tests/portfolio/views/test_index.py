import pytest
from django.urls import reverse

from portfolio.models.booking_config import BookingConfig
from portfolio.models.service import Service


@pytest.mark.django_db
class TestHomeView:
    
    def test_view_url_exists_at_desired_location(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200


    def test_view_uses_correct_template(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'portfolio/index.html' in [t.name for t in response.templates]


    def test_context_has_business_config(self, client, business_config):
        response = client.get(reverse('home'))
        assert response.context['config'] == business_config
        assert response.context['config'].site_name == "Julia Ellen Nails"


    def test_context_handles_missing_config(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert response.context['config'] is None


    def test_context_services_filtering(self, client, service_manicure):
        inactive_service = Service.objects.create(
            title="Serviço Desativado",
            description="Não deve aparecer",
            price=10.00,
            active=False
        )

        response = client.get(reverse('home'))
        services_in_context = response.context['services']

        assert service_manicure in services_in_context
        
        assert inactive_service not in services_in_context
        assert services_in_context.count() == 1


    def test_context_portfolio_items(self, client, portfolio_item):
        """Verifica se os itens de portfólio são carregados."""
        response = client.get(reverse('home'))
        items = response.context['portfolio_items']
        
        assert portfolio_item in items
        assert items.count() == 1


    def test_context_schedules(self, client):
        b1 = BookingConfig.objects.create(schedule="Manhã")
        b2 = BookingConfig.objects.create(schedule="Tarde")

        response = client.get(reverse('home'))
        schedules = response.context['schedules']

        assert b1 in schedules
        assert b2 in schedules
        assert schedules.count() == 2

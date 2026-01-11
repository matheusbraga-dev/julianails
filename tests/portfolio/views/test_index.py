import pytest
from django.urls import reverse

from portfolio.models.booking_config import BookingConfig
from portfolio.models.service import Service
from portfolio.models.visit import Visit


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


    url = reverse('home') 

    def test_first_visit_increments_counter(self, client):
        initial_count = Visit.objects.count()
        response = client.get(self.url)

        assert response.status_code == 200
        assert Visit.objects.count() == initial_count + 1
        
        visit = Visit.objects.first()
        assert visit.ip_address == "127.0.0.1"

        assert client.session.get('has_visited') is True

    def test_second_visit_does_not_increment_counter(self, client):
        client.get(self.url)
        assert Visit.objects.count() == 1
        
        client.get(self.url)
        assert Visit.objects.count() == 1

    def test_visit_records_real_ip_via_remote_addr(self, client):
        response = client.get(self.url, REMOTE_ADDR="10.0.0.5")

        visit = Visit.objects.first()
        assert visit is not None

    def test_visit_records_ip_via_x_forwarded_for(self, client):
        headers = {'HTTP_X_FORWARDED_FOR': '203.0.113.195, 192.168.1.1'}
        client.get(self.url, **headers)
        visit = Visit.objects.first()
        assert visit.ip_address == '203.0.113.195'

    def test_new_session_creates_new_visit(self, client):
        client.get(self.url)
        assert Visit.objects.count() == 1
        
        client.cookies.clear() 
        client.get(self.url)
        assert Visit.objects.count() == 2

    def test_session_expiry_set_correctly(self, client):
        client.get(self.url)
        session = client.session
        expiry_age = session.get_expiry_age()
        
        assert 86400 - 5 <= expiry_age <= 86400 + 5

import pytest
from portfolio.models.visit import Visit


@pytest.mark.django_db
class TestVisitModel:
    
    def test_visit_creation(self):
        visit = Visit.objects.create(ip_address="192.168.0.1", page="Home")
        
        assert visit.id is not None
        assert visit.ip_address == "192.168.0.1"
        assert visit.timestamp is not None

    def test_visit_string_representation(self):
        visit = Visit.objects.create(ip_address="127.0.0.1")
        assert "Acesso em" in str(visit)

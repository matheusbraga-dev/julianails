import pytest
from django.core.exceptions import ValidationError
from portfolio.models.business_config import BusinessConfig


@pytest.mark.django_db
def test_singleton_prevent_duplicates(business_config):
    with pytest.raises(ValidationError) as excinfo:
        BusinessConfig.objects.create(
            site_name="Site Falso",
            phone_display="(11) 00000-0000",
            whatsapp_number="5511000000000",
            instagram_handle="fake",
            about_text_p1="Fake"
        )
    
    assert "Já existe um registro de Configuração do Site" in str(excinfo.value)


@pytest.mark.django_db
def test_singleton_allows_update(business_config):
    business_config.site_name = "Novo Nome Atualizado"
    business_config.save() 
    
    business_config.refresh_from_db()
    assert business_config.site_name == "Novo Nome Atualizado"


@pytest.mark.django_db
def test_create_first_instance(db):
    assert BusinessConfig.objects.count() == 0
    
    conf = BusinessConfig.objects.create(
        site_name="Primeira Config",
        phone_display="123",
        whatsapp_number="123",
        instagram_handle="insta",
        about_text_p1="About"
    )
    assert conf.pk is not None
    assert BusinessConfig.objects.count() == 1



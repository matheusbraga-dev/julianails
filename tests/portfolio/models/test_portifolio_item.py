import pytest
import time

@pytest.mark.django_db
def test_timestamps_update(portfolio_item):
    assert portfolio_item.created_at is not None
    assert portfolio_item.updated_at is not None
    
    original_created_at = portfolio_item.created_at
    original_updated_at = portfolio_item.updated_at

    time.sleep(0.1)

    portfolio_item.title = "Unha Gel Editada"
    portfolio_item.save()
    

    portfolio_item.refresh_from_db()

    assert portfolio_item.updated_at > original_updated_at
    assert portfolio_item.created_at == original_created_at

from django.views.generic import TemplateView
from .models import business_config, service, portfolio_item, booking_config


class HomeView(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['config'] = business_config.BusinessConfig.objects.first()

        context['services'] = service.Service.objects.filter(active=True)

        context['portfolio_items'] = portfolio_item.PortfolioItem.objects.all()
        
        context['schedules'] = booking_config.BookingConfig.objects.all()

        return context

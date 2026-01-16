from django.views.generic import TemplateView

from .models import (
    business_config,
    service,
    portfolio_item,
    booking_config,
)

from .services.calendar import CalendarService
from .services.visit import VisitService


class HomeView(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['config'] = business_config.BusinessConfig.objects.first()

        context['services'] = service.Service.objects.filter(active=True)

        context['portfolio_items'] = portfolio_item.PortfolioItem.objects.all()
        
        context['schedules'] = booking_config.BookingConfig.objects.all()
       
        context.update(CalendarService.get_calendar_context())
    
        return context
    
    def get(self, request, *args, **kwargs):
        VisitService.track_visit(request, page_name="Home")

        return super().get(request, *args, **kwargs)

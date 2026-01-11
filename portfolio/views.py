from django.views.generic import TemplateView
from .models import business_config, service, portfolio_item, booking_config, visit


class HomeView(TemplateView):
    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['config'] = business_config.BusinessConfig.objects.first()

        context['services'] = service.Service.objects.filter(active=True)

        context['portfolio_items'] = portfolio_item.PortfolioItem.objects.all()
        
        context['schedules'] = booking_config.BookingConfig.objects.all()

        return context
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('has_visited'):
    
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            visit.Visit.objects.create(ip_address=ip, page="Home")
            
            request.session['has_visited'] = True
            request.session.set_expiry(60 * 60 * 24)

        return super().get(request, *args, **kwargs)

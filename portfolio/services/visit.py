from ..models import visit


class VisitService:
    """Responsável por rastrear visitas únicas baseadas em sessão e IP."""

    EXPIRED_SESSION_SECONDS = 60 * 60 * 24

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @classmethod
    def track_visit(cls, request, page_name="Home"):
        if request.session.get('has_visited'):
            return

        ip = cls.get_client_ip(request)
        
        visit.Visit.objects.create(ip_address=ip, page=page_name)
        
        request.session['has_visited'] = True
        request.session.set_expiry(cls.EXPIRED_SESSION_SECONDS)
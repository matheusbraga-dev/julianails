import calendar
import json
from datetime import timedelta
from django.utils import timezone
from ..models import schedule_config

class CalendarService:
    """Responsável por toda lógica de datas, bloqueios e dias úteis."""

    @staticmethod
    def get_calendar_settings():
        settings, _ = schedule_config.ScheduleConfig.objects.get_or_create(id=1)
        return settings

    @classmethod
    def get_calendar_context(cls):
        settings = cls.get_calendar_settings()
        today = timezone.localdate()

        # 1. Lógica da Data Máxima
        if settings.only_current_month:
            last_day = calendar.monthrange(today.year, today.month)[1]
            max_date = today.replace(day=last_day)
        else:
            max_date = today + timedelta(days=settings.max_days_ahead)

        # 2. Lógica dos Dias da Semana Desativados
        disabled_weekdays = []
        if not settings.works_sunday: disabled_weekdays.append(0)
        if not settings.works_monday: disabled_weekdays.append(1)
        if not settings.works_tuesday: disabled_weekdays.append(2)
        if not settings.works_wednesday: disabled_weekdays.append(3)
        if not settings.works_thursday: disabled_weekdays.append(4)
        if not settings.works_friday: disabled_weekdays.append(5)
        if not settings.works_saturday: disabled_weekdays.append(6)

        # 3. Lógica de Intervalos Bloqueados (Feriados/Férias)
        blocked_ranges = schedule_config.BlockedDate.objects.filter(end_date__gte=today)
        blocked_dates = []
        
        for item in blocked_ranges:
            current = max(item.start_date, today)
            while current <= item.end_date:
                blocked_dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

        return {
            "calendar_max_date": max_date.strftime("%Y-%m-%d"),
            "calendar_disable_weekdays": json.dumps(disabled_weekdays),
            "calendar_blocked_dates": json.dumps(blocked_dates),
        }

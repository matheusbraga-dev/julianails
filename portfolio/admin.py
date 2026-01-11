from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.auth.models import Group
from .models import business_config, service, portfolio_item, booking_config, visit


admin.site.unregister(Group)


@admin.register(business_config.BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    """
    Configuração para garantir que exista apenas 1 registro de configuração
    e organizar os campos em abas/seções.
    """ 
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("site_name", "phone_display", "whatsapp_number", "instagram_handle", "address", "opening_days", "opening_hours", "hero_image"),
        }),
        ("Seção Sobre", {
            "fields": ("about_image", "preview_image", "about_text_p1", "about_text_p2"),
            "description": "Edite aqui a foto e os textos que aparecem na janela 'Sobre Mim'."
        }),
    )
    readonly_fields = ["preview_image"]

    def preview_image(self, obj):
        if obj.about_image:
            return mark_safe(f'<img src="{obj.about_image.url}" width="150" style="border-radius:10px;"/>')
        return "Sem imagem"
    preview_image.short_description = "Pré-visualização da Foto Atual"


    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(service.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "is_sale", "is_popular", "active", "icon_display")
    list_editable = ("price", "active", "is_sale", "is_popular")
    list_filter = ("active", "is_sale", "is_popular")
    search_fields = ("title",)
    
    fieldsets = (
        (None, {
            "fields": ("title", "description", "price")
        }),
        ("Aparência e Destaque", {
            "fields": ("icon", "is_sale", "is_popular", "active"),
            "classes": ("collapse",),
        }),
    )

    def icon_display(self, obj):
        return mark_safe(f'<i class="fas {obj.icon}" style="font-size: 1.2em; color: #b474c6;"></i>')
    icon_display.short_description = "Ícone"

@admin.register(portfolio_item.PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "title", "created_at")
    search_fields = ("title",)
    list_per_page = 10

    def thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover; border-radius:5px;" />')
        return "-"
    thumbnail.short_description = "Foto"

@admin.register(booking_config.BookingConfig)
class BookingConfigAdmin(admin.ModelAdmin):
    list_display = ('schedule',)
    search_fields = ('schedule',)
    list_per_page = 10
    fieldsets = (
        (None, {
            "fields": ("schedule",),
        }),
    )

    def icon_display(self, obj):
        return mark_safe(f'<i class="fas {obj.icon}" style="font-size: 1.2em; color: #b474c6;"></i>')
    icon_display.short_description = "Ícone"


@admin.register(visit.Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'ip_address', 'page')
    list_filter = ('timestamp', 'page')
    date_hierarchy = 'timestamp'
    search_fields = ('ip_address',)
    
    change_list_template = 'portfolio/admin/portfolio/visit/change_list.html'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        if hasattr(response, 'context_data') and 'cl' in response.context_data:
            qs = response.context_data['cl'].queryset
            total = qs.count()
            unique = qs.values('ip_address').distinct().count()

            response.context_data['total_visits'] = total
            response.context_data['unique_visitors'] = unique
        
        return response

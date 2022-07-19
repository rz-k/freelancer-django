from django.contrib import admin
from .models import PricingPanel, ActivePricingPanel, PricingTag


@admin.register(PricingTag)
class PricingTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    
@admin.register(ActivePricingPanel)
class ActivePricingPanelAdmin(admin.ModelAdmin):
    list_display = ['user', 'active_panel', 'count', 'expire_time']
    
@admin.register(PricingPanel)
class PricingPanelAdmin(admin.ModelAdmin):
    list_display = ['panel_type', 'price', 'count', 'days', 'position']

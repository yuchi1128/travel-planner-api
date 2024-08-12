from django.contrib import admin
from .models import Destination, TravelPlan

# Destinationモデルの管理クラス
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

# TravelPlanモデルの管理クラス
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ('destination', 'days', 'weather_forecast', 'plan_details')
    list_filter = ('destination', 'days')
    search_fields = ('destination__name',)

# 管理画面にモデルを登録
admin.site.register(Destination, DestinationAdmin)
admin.site.register(TravelPlan, TravelPlanAdmin)

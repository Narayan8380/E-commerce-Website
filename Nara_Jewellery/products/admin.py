from django.contrib import admin
from .models import Category, Product, VisitRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('id', 'product_name', 'category',
                     'price', 'stock_quantity', 'created_at')
    list_filter   = ('category',)
    search_fields = ('product_name',)


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'phone', 'product',
                     'preferred_date', 'preferred_time',
                     'status', 'created_at')
    list_filter   = ('status',)
    search_fields = ('name', 'phone')
    list_editable = ('status',)
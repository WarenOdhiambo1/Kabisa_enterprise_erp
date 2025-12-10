from django.contrib import admin
from .models import Branch, Employee, Product, Stock, StockMovement, Order, OrderItem, Sale, SaleItem


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'address', 'email']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'position', 'is_active']
    list_filter = ['is_active', 'branches']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['branches']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'unit_price', 'cost_price', 'category', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'sku', 'description']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'branch', 'quantity', 'min_quantity', 'is_low_stock']
    list_filter = ['branch']
    search_fields = ['product__name', 'branch__name']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['stock', 'movement_type', 'quantity', 'status', 'created_at']
    list_filter = ['movement_type', 'status']
    search_fields = ['stock__product__name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'branch', 'supplier', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'branch']
    search_fields = ['order_number', 'supplier']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'subtotal']
    search_fields = ['product_name', 'order__order_number']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'branch', 'customer_name', 'total_amount', 'payment_method', 'created_at']
    list_filter = ['branch', 'payment_method']
    search_fields = ['sale_number', 'customer_name']


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'stock', 'quantity', 'unit_price', 'subtotal']
    search_fields = ['sale__sale_number']

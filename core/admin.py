from django.contrib import admin
from .models import (
    Branch, Employee, Product, Stock, StockMovement, Order, OrderItem, 
    Sale, SaleItem, UserProfile, Expense, Logistics, Vehicle, Trip, VehicleMaintenance
)


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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'branch', 'phone']
    list_filter = ['role', 'branch']
    search_fields = ['user__username', 'user__email']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'branch', 'expense_type', 'amount', 'expense_date', 'sale']
    list_filter = ['expense_type', 'branch', 'expense_date']
    search_fields = ['expense_number', 'description']


@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'customer_name', 'from_branch', 'vehicle', 'driver', 'status', 'delivery_date', 'delivery_cost']
    list_filter = ['status', 'from_branch', 'vehicle']
    search_fields = ['tracking_number', 'customer_name', 'customer_phone']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'vehicle_type', 'make', 'model', 'year', 'branch', 'assigned_driver', 'status', 'current_mileage']
    list_filter = ['status', 'vehicle_type', 'branch']
    search_fields = ['registration_number', 'make', 'model']
    readonly_fields = ['total_trips', 'total_revenue', 'total_maintenance_cost', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('registration_number', 'vehicle_type', 'make', 'model', 'year', 'color')
        }),
        ('Assignment', {
            'fields': ('branch', 'assigned_driver', 'status')
        }),
        ('Tracking', {
            'fields': ('current_mileage', 'fuel_capacity')
        }),
        ('Financial', {
            'fields': ('purchase_price', 'purchase_date', 'total_revenue', 'total_maintenance_cost')
        }),
        ('Compliance', {
            'fields': ('insurance_expiry', 'registration_expiry')
        }),
        ('Additional Info', {
            'fields': ('notes', 'total_trips', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['trip_number', 'vehicle', 'driver', 'trip_type', 'origin', 'destination', 'status', 'scheduled_date', 'revenue', 'net_profit']
    list_filter = ['status', 'trip_type', 'vehicle', 'scheduled_date']
    search_fields = ['trip_number', 'origin', 'destination', 'customer_name']
    readonly_fields = ['net_profit', 'duration', 'created_at', 'updated_at']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('trip_number', 'vehicle', 'driver', 'trip_type', 'status')
        }),
        ('Route Details', {
            'fields': ('origin', 'destination', 'distance')
        }),
        ('Related Records', {
            'fields': ('sale', 'logistics')
        }),
        ('Schedule & Timing', {
            'fields': ('scheduled_date', 'start_time', 'end_time', 'duration')
        }),
        ('Financial', {
            'fields': ('revenue', 'fuel_cost', 'other_expenses', 'net_profit')
        }),
        ('Mileage Tracking', {
            'fields': ('start_mileage', 'end_mileage')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_phone'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['maintenance_number', 'vehicle', 'maintenance_type', 'service_date', 'status', 'total_cost', 'service_provider']
    list_filter = ['status', 'maintenance_type', 'service_date', 'vehicle']
    search_fields = ['maintenance_number', 'vehicle__registration_number', 'service_provider', 'description']
    readonly_fields = ['total_cost', 'created_at', 'updated_at']
    date_hierarchy = 'service_date'
    
    fieldsets = (
        ('Maintenance Information', {
            'fields': ('maintenance_number', 'vehicle', 'maintenance_type', 'status')
        }),
        ('Service Details', {
            'fields': ('description', 'service_provider', 'service_date', 'completion_date')
        }),
        ('Costs', {
            'fields': ('parts_cost', 'labor_cost', 'other_costs', 'total_cost', 'receipt_number')
        }),
        ('Mileage Tracking', {
            'fields': ('mileage_at_service', 'next_service_mileage')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

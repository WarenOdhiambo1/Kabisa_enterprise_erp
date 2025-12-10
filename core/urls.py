from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Branches
    path('branches/', views.branch_list, name='branch_list'),
    path('branches/create/', views.branch_create, name='branch_create'),
    path('branches/<int:pk>/', views.branch_detail, name='branch_detail'),
    path('branches/<int:pk>/edit/', views.branch_edit, name='branch_edit'),
    path('branches/<int:pk>/delete/', views.branch_delete, name='branch_delete'),
    
    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Stock
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/add/', views.stock_create, name='stock_create'),
    path('stock/movements/', views.stock_movement_list, name='stock_movement_list'),
    path('stock/transfer/', views.stock_transfer, name='stock_transfer'),
    path('stock/transfer/<int:pk>/approve/', views.approve_transfer, name='approve_transfer'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/complete/', views.order_complete, name='order_complete'),
    
    # Sales
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/create/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    
    # Expenses
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/create/', views.expense_create, name='expense_create'),
    
    # Logistics
    path('logistics/', views.logistics_list, name='logistics_list'),
    path('logistics/create/', views.logistics_create, name='logistics_create'),
    path('logistics/<int:pk>/update/', views.logistics_update_status, name='logistics_update_status'),
    
    # Finance
    path('finance/reports/', views.financial_reports, name='financial_reports'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    
    # Vehicles
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    
    # Trips
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create/', views.trip_create, name='trip_create'),
    
    # Maintenance
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    
    # API
    path('api/branch/<int:branch_id>/stocks/', views.get_branch_stocks, name='get_branch_stocks'),
]

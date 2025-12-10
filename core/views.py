from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse
from decimal import Decimal
import uuid

from .models import Branch, Employee, Product, Stock, StockMovement, Order, OrderItem, Sale, SaleItem


def dashboard(request):
    branches = Branch.objects.filter(is_active=True)
    total_branches = branches.count()
    total_employees = Employee.objects.filter(is_active=True).count()
    total_products = Product.objects.filter(is_active=True).count()
    
    total_sales = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    recent_sales = Sale.objects.select_related('branch')[:5]
    recent_orders = Order.objects.select_related('branch')[:5]
    
    low_stock_items = Stock.objects.filter(quantity__lte=models.F('min_quantity')).select_related('product', 'branch')[:10]
    pending_orders = Order.objects.filter(status='PENDING').count()
    pending_transfers = StockMovement.objects.filter(movement_type='TRANSFER', status='PENDING').count()
    
    context = {
        'total_branches': total_branches,
        'total_employees': total_employees,
        'total_products': total_products,
        'total_sales': total_sales,
        'recent_sales': recent_sales,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
        'pending_orders': pending_orders,
        'pending_transfers': pending_transfers,
    }
    return render(request, 'core/dashboard.html', context)


def branch_list(request):
    search = request.GET.get('search', '')
    branches = Branch.objects.all()
    if search:
        branches = branches.filter(Q(name__icontains=search) | Q(address__icontains=search))
    return render(request, 'core/branch_list.html', {'branches': branches, 'search': search})


def branch_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        
        Branch.objects.create(name=name, address=address, phone=phone, email=email)
        messages.success(request, 'Branch created successfully!')
        return redirect('branch_list')
    return render(request, 'core/branch_form.html', {'action': 'Create'})


def branch_edit(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        branch.name = request.POST.get('name')
        branch.address = request.POST.get('address', '')
        branch.phone = request.POST.get('phone', '')
        branch.email = request.POST.get('email', '')
        branch.is_active = request.POST.get('is_active') == 'on'
        branch.save()
        messages.success(request, 'Branch updated successfully!')
        return redirect('branch_list')
    return render(request, 'core/branch_form.html', {'branch': branch, 'action': 'Edit'})


def branch_delete(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        branch.delete()
        messages.success(request, 'Branch deleted successfully!')
    return redirect('branch_list')


def employee_list(request):
    search = request.GET.get('search', '')
    employees = Employee.objects.prefetch_related('branches').all()
    if search:
        employees = employees.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) | 
            Q(email__icontains=search)
        )
    return render(request, 'core/employee_list.html', {'employees': employees, 'search': search})


def employee_create(request):
    branches = Branch.objects.filter(is_active=True)
    if request.method == 'POST':
        employee = Employee.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            position=request.POST.get('position', ''),
        )
        branch_ids = request.POST.getlist('branches')
        employee.branches.set(branch_ids)
        messages.success(request, 'Employee created successfully!')
        return redirect('employee_list')
    return render(request, 'core/employee_form.html', {'branches': branches, 'action': 'Create'})


def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    branches = Branch.objects.filter(is_active=True)
    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone', '')
        employee.position = request.POST.get('position', '')
        employee.is_active = request.POST.get('is_active') == 'on'
        employee.save()
        branch_ids = request.POST.getlist('branches')
        employee.branches.set(branch_ids)
        messages.success(request, 'Employee updated successfully!')
        return redirect('employee_list')
    return render(request, 'core/employee_form.html', {'employee': employee, 'branches': branches, 'action': 'Edit'})


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
    return redirect('employee_list')


def product_list(request):
    search = request.GET.get('search', '')
    products = Product.objects.all()
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(sku__icontains=search) | 
            Q(category__icontains=search)
        )
    return render(request, 'core/product_list.html', {'products': products, 'search': search})


def product_create(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            sku=request.POST.get('sku'),
            description=request.POST.get('description', ''),
            unit_price=Decimal(request.POST.get('unit_price', '0')),
            cost_price=Decimal(request.POST.get('cost_price', '0')),
            category=request.POST.get('category', ''),
        )
        messages.success(request, 'Product created successfully!')
        return redirect('product_list')
    return render(request, 'core/product_form.html', {'action': 'Create'})


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.description = request.POST.get('description', '')
        product.unit_price = Decimal(request.POST.get('unit_price', '0'))
        product.cost_price = Decimal(request.POST.get('cost_price', '0'))
        product.category = request.POST.get('category', '')
        product.is_active = request.POST.get('is_active') == 'on'
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')
    return render(request, 'core/product_form.html', {'product': product, 'action': 'Edit'})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')


def stock_list(request):
    search = request.GET.get('search', '')
    branch_id = request.GET.get('branch', '')
    stocks = Stock.objects.select_related('product', 'branch').all()
    
    if search:
        stocks = stocks.filter(
            Q(product__name__icontains=search) | 
            Q(product__sku__icontains=search)
        )
    if branch_id:
        stocks = stocks.filter(branch_id=branch_id)
    
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'core/stock_list.html', {
        'stocks': stocks, 
        'branches': branches,
        'search': search,
        'selected_branch': branch_id
    })


def stock_create(request):
    branches = Branch.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 0))
        min_quantity = int(request.POST.get('min_quantity', 10))
        
        stock, created = Stock.objects.get_or_create(
            branch_id=branch_id,
            product_id=product_id,
            defaults={'quantity': quantity, 'min_quantity': min_quantity}
        )
        if not created:
            stock.quantity += quantity
            stock.min_quantity = min_quantity
            stock.save()
        
        messages.success(request, 'Stock updated successfully!')
        return redirect('stock_list')
    return render(request, 'core/stock_form.html', {
        'branches': branches, 
        'products': products,
        'action': 'Add'
    })


def stock_movement_list(request):
    search = request.GET.get('search', '')
    movements = StockMovement.objects.select_related('stock__product', 'stock__branch', 'from_branch', 'to_branch').all()
    
    if search:
        movements = movements.filter(
            Q(stock__product__name__icontains=search) | 
            Q(notes__icontains=search)
        )
    
    return render(request, 'core/stock_movement_list.html', {'movements': movements, 'search': search})


def stock_transfer(request):
    branches = Branch.objects.filter(is_active=True)
    if request.method == 'POST':
        from_branch_id = request.POST.get('from_branch')
        to_branch_id = request.POST.get('to_branch')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 0))
        notes = request.POST.get('notes', '')
        
        from_branch = get_object_or_404(Branch, pk=from_branch_id)
        to_branch = get_object_or_404(Branch, pk=to_branch_id)
        product = get_object_or_404(Product, pk=product_id)
        
        stock = get_object_or_404(Stock, branch=from_branch, product=product)
        
        if stock.quantity < quantity:
            messages.error(request, 'Insufficient stock for transfer!')
            return redirect('stock_transfer')
        
        StockMovement.objects.create(
            stock=stock,
            movement_type='TRANSFER',
            quantity=quantity,
            from_branch=from_branch,
            to_branch=to_branch,
            status='PENDING',
            notes=notes
        )
        
        messages.success(request, 'Transfer request created. Awaiting approval.')
        return redirect('stock_movement_list')
    
    products = Product.objects.filter(is_active=True)
    return render(request, 'core/stock_transfer_form.html', {
        'branches': branches,
        'products': products
    })


def approve_transfer(request, pk):
    movement = get_object_or_404(StockMovement, pk=pk, movement_type='TRANSFER', status='PENDING')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            movement.status = 'APPROVED'
            movement.stock.quantity -= movement.quantity
            movement.stock.save()
            
            to_stock, created = Stock.objects.get_or_create(
                branch=movement.to_branch,
                product=movement.stock.product,
                defaults={'quantity': 0}
            )
            to_stock.quantity += movement.quantity
            to_stock.save()
            
            movement.save()
            messages.success(request, 'Transfer approved!')
        else:
            movement.status = 'REJECTED'
            movement.save()
            messages.info(request, 'Transfer rejected.')
    return redirect('stock_movement_list')


def order_list(request):
    search = request.GET.get('search', '')
    orders = Order.objects.select_related('branch').prefetch_related('items').all()
    
    if search:
        orders = orders.filter(
            Q(order_number__icontains=search) | 
            Q(supplier__icontains=search)
        )
    
    return render(request, 'core/order_list.html', {'orders': orders, 'search': search})


def order_create(request):
    branches = Branch.objects.filter(is_active=True)
    if request.method == 'POST':
        order = Order.objects.create(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            branch_id=request.POST.get('branch'),
            supplier=request.POST.get('supplier', ''),
            notes=request.POST.get('notes', ''),
        )
        
        product_names = request.POST.getlist('product_name')
        product_skus = request.POST.getlist('product_sku')
        quantities = request.POST.getlist('quantity')
        unit_prices = request.POST.getlist('unit_price')
        
        for i in range(len(product_names)):
            if product_names[i]:
                OrderItem.objects.create(
                    order=order,
                    product_name=product_names[i],
                    product_sku=product_skus[i] if i < len(product_skus) else '',
                    quantity=int(quantities[i]) if i < len(quantities) else 1,
                    unit_price=Decimal(unit_prices[i]) if i < len(unit_prices) else Decimal('0'),
                )
        
        order.calculate_total()
        messages.success(request, f'Order {order.order_number} created!')
        return redirect('order_list')
    
    return render(request, 'core/order_form.html', {'branches': branches, 'action': 'Create'})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'core/order_detail.html', {'order': order})


def order_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'COMPLETED'
        order.save()
        
        for item in order.items.all():
            stock, created = Stock.objects.get_or_create(
                branch=order.branch,
                product=item.product,
                defaults={'quantity': 0}
            )
            stock.quantity += item.quantity
            stock.save()
            
            StockMovement.objects.create(
                stock=stock,
                movement_type='IN',
                quantity=item.quantity,
                status='APPROVED',
                notes=f"Order #{order.order_number} completed"
            )
        
        messages.success(request, f'Order {order.order_number} completed! Stock updated.')
    return redirect('order_list')


def sale_list(request):
    search = request.GET.get('search', '')
    sales = Sale.objects.select_related('branch').prefetch_related('items__stock__product').all()
    
    if search:
        sales = sales.filter(
            Q(sale_number__icontains=search) | 
            Q(customer_name__icontains=search)
        )
    
    return render(request, 'core/sale_list.html', {'sales': sales, 'search': search})


def sale_create(request):
    branches = Branch.objects.filter(is_active=True)
    
    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        sale = Sale.objects.create(
            sale_number=f"SALE-{uuid.uuid4().hex[:8].upper()}",
            branch_id=branch_id,
            customer_name=request.POST.get('customer_name', ''),
            customer_phone=request.POST.get('customer_phone', ''),
            payment_method=request.POST.get('payment_method', 'Cash'),
            notes=request.POST.get('notes', ''),
        )
        
        stock_ids = request.POST.getlist('stock_id')
        quantities = request.POST.getlist('quantity')
        unit_prices = request.POST.getlist('unit_price')
        
        for i in range(len(stock_ids)):
            if stock_ids[i]:
                stock = get_object_or_404(Stock, pk=stock_ids[i])
                qty = int(quantities[i]) if i < len(quantities) else 1
                price = Decimal(unit_prices[i]) if i < len(unit_prices) else stock.product.unit_price
                
                SaleItem.objects.create(
                    sale=sale,
                    stock=stock,
                    quantity=qty,
                    unit_price=price,
                )
        
        sale.calculate_total()
        messages.success(request, f'Sale {sale.sale_number} created!')
        return redirect('sale_list')
    
    return render(request, 'core/sale_form.html', {'branches': branches, 'action': 'Create'})


def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'core/sale_detail.html', {'sale': sale})


def get_branch_stocks(request, branch_id):
    stocks = Stock.objects.filter(branch_id=branch_id, quantity__gt=0).select_related('product')
    data = [
        {
            'id': s.id,
            'product_name': s.product.name,
            'product_sku': s.product.sku,
            'quantity': s.quantity,
            'unit_price': str(s.product.unit_price)
        }
        for s in stocks
    ]
    return JsonResponse(data, safe=False)


from django.db import models

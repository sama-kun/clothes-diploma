from django.shortcuts import render
from shop.models import Category, Customer, Product, Cart

def products(request):
    current_user = request.user
    customer = Customer.objects.filter(user_id=current_user.id).first()

    categories = Category.objects.all()
    categoryid = request.GET.get('category', 0)

    # Filter products by category if selected
    products = Product.objects.all()
    filtered_category = None
    if categoryid:
        filtered_category = Category.objects.filter(id=categoryid).first()
        products = products.filter(category_id=categoryid)

    # Filter products by selected price range
    min_price = products.order_by('price').first().price if products.exists() else 0
    max_price = products.order_by('-price').first().price if products.exists() else 0

    min_selected_price = int(request.GET.get('min_price', min_price))
    max_selected_price = int(request.GET.get('max_price', max_price))
    
    # Apply price filtering
    products = products.filter(price__gte=min_selected_price, price__lte=max_selected_price)

    # Sorting functionality
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('product_name')
    elif sort_by == 'name_desc':
        products = products.order_by('-product_name')

    # Additional data for cart and user info
    carts = Cart.objects.filter(user_id=current_user.id)
    qty = sum(cart.qty for cart in carts)
    total = sum(cart.amount for cart in carts)

    # Set the product title based on the filtered category
    product_title = filtered_category.category_name if filtered_category else "All products"

    # Pass everything to the template
    params = {
        'customer': customer,
        'products': products,
        'categories': categories,
        'filtered_category': filtered_category,
        'n': products.count(),
        'qty': qty,
        'total': total,
        'carts': carts,
        'min_price': min_price,
        'max_price': max_price,
        'min_selected_price': min_selected_price,
        'max_selected_price': max_selected_price,
        'product_title': product_title,
    }
    
    return render(request, 'products.html', params)

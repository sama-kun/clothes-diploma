from django.shortcuts import render
from shop.models import Category, Customer, Product, Cart, Wishlist, Department, Gender

def products(request):
    current_user = request.user
    customer = Customer.objects.filter(user_id=current_user.id).first()

    # Retrieve all genders
    genders = Gender.objects.all()
    gender_id = request.GET.get('gender', None)

    # Get selected departments and categories (multiple selection)
    selected_departments = request.GET.getlist('departments')
    selected_categories = request.GET.getlist('categories')

    # Filter departments by selected gender
    if gender_id:
        departments = Department.objects.filter(genders__id=gender_id)
    else:
        departments = Department.objects.all()

    # Filter categories by selected gender and departments
    if gender_id:
        if selected_departments:
            categories = Category.objects.filter(
                genders__id=gender_id,
                departments__id__in=selected_departments
            ).distinct()
        else:
            categories = Category.objects.filter(
                genders__id=gender_id
            ).distinct()
    else:
        if selected_departments:
            categories = Category.objects.filter(
                departments__id__in=selected_departments
            ).distinct()
        else:
            categories = Category.objects.all()

    # Filter products by selected filters (gender, departments, categories)
    products = Product.objects.all()
    if gender_id:
        products = products.filter(gender_id=gender_id)
    if selected_departments:
        products = products.filter(category__departments__id__in=selected_departments)
    if selected_categories:
        products = products.filter(category_id__in=selected_categories)

    # Calculate local min/max price for the filtered products
    if products.exists():
        local_min_price = products.order_by('price').first().price
        local_max_price = products.order_by('-price').first().price
    else:
        local_min_price = 0
        local_max_price = 0

    # Determine if price filters should be reset (e.g., when other filters change)
    reset_price_filter = (
        'gender' in request.GET or
        'departments' in request.GET or
        'categories' in request.GET
    )

    # If the price filter needs to be reset, use the local min/max prices
    if reset_price_filter:
        min_selected_price = local_min_price
        max_selected_price = local_max_price
    else:
        # Otherwise, get price values from the request and ensure they're within the local range
        min_selected_price = int(request.GET.get('min_price', local_min_price))
        max_selected_price = int(request.GET.get('max_price', local_max_price))

    # Apply price filter to products
    products = products.filter(price__gte=min_selected_price, price__lte=max_selected_price)

    # Sorting products
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('product_name')
    elif sort_by == 'name_desc':
        products = products.order_by('-product_name')

    # Wishlist logic
    liked_product_ids = set(Wishlist.objects.filter(user=current_user).values_list('product_id', flat=True))
    for product in products:
        product.liked = product.id in liked_product_ids

    # Cart data
    carts = Cart.objects.filter(user_id=current_user.id)
    qty = sum(cart.qty for cart in carts)
    total = sum(cart.amount for cart in carts)

    # Title construction based on selected filters
    product_title = "Products"
    if gender_id:
        product_title = Gender.objects.get(id=gender_id).name
    if selected_departments:
        department_names = ", ".join(
            Department.objects.filter(id__in=selected_departments).values_list('department_name', flat=True)
        )
        product_title += f" > {department_names}"
    if selected_categories:
        category_names = ", ".join(
            Category.objects.filter(id__in=selected_categories).values_list('category_name', flat=True)
        )
        product_title += f" > {category_names}"

    # Prepare data for filters
    params = {
        'customer': customer,
        'products': products,
        'gendersFilters': genders,
        'departments': departments,
        'categories': categories,
        'n': products.count(),
        'qty': qty,
        'total': total,
        'carts': carts,
        'local_min_price': local_min_price,  # Local minimum price for current filter
        'local_max_price': local_max_price,  # Local maximum price for current filter
        'min_selected_price': min_selected_price,  # Selected minimum price
        'max_selected_price': max_selected_price,  # Selected maximum price
        'product_title': product_title,
        'selected_gender': int(gender_id) if gender_id else None,
        'selected_departments': [int(dept) for dept in selected_departments],
        'selected_categories': [int(cat) for cat in selected_categories],
    }

    return render(request, 'products.html', params)
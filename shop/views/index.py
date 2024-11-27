from django.shortcuts import render
from shop.models import Category, Customer, Gender, Product, Cart

def index(request):
    current_user = request.user
    products = Product.objects.all()
    mobiles = Product.objects.filter(category_id=1)
    laptops = Product.objects.filter(category_id=2)
    tvs = Product.objects.filter(category_id=3)
    headphones = Product.objects.filter(category_id=6)
    homeapps = Product.objects.filter(category_id=9)
    kitapps = Product.objects.filter(category_id=8)
    categories = Category.objects.all()
    carts = Cart.objects.filter(user_id=current_user.id)

    # Prefetching the related data to minimize database hits
    genders = Gender.objects.prefetch_related('departments', 'categories')
    gender_data = []

    for gender in genders:
        departments = gender.departments.all()  # Get departments related to gender
        department_data = []
        
        for department in departments:
            # Categories related to both gender and department
            categories = department.categories.filter(genders=gender)
            department_data.append({
                'department_id': department.id,  # Add department id
                'department_name': department.department_name,
                'categories': [{'category_name': cat.category_name, 'category_id': cat.id} for cat in categories]  # Add category id
            })
        
        gender_data.append({
            'gender_id': gender.id,  # Add gender id
            'gender_name': gender.name,
            'departments': department_data
        })

    # Getting the current user's customer object
    try:
        customer = Customer.objects.get(user_id=current_user.id)
    except Customer.DoesNotExist:
        customer = None
    
    qty = 0
    total = 0
    for cart in carts:
        total += cart.amount
        qty += cart.qty

    params = {
        'customer': customer,
        'products': products,
        'mobiles': mobiles,
        'laptops': laptops,
        'tvs': tvs,
        'headphones': headphones,
        'homeapps': homeapps,
        'kitapps': kitapps,
        'categories': categories,
        'qty': qty,
        'total': total,
        'carts': carts,
        'genders': gender_data,  # Include gender data with ids
    }

    return render(request, 'index.html', params)

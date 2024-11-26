from django.views import View
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

    genders = Gender.objects.prefetch_related('departments', 'categories')
    gender_data = []
    for gender in genders:
        departments = gender.departments.all()  # Департаменты, относящиеся к гендеру
        department_data = []
        for department in departments:
            categories = department.categories.filter(genders=gender)  # Категории, относящиеся и к гендеру, и к департаменту
            department_data.append({
                'department_name': department.department_name,
                'categories': [{'category_name': cat.category_name} for cat in categories]
            })
        gender_data.append({
            'gender_name': gender.name,
            'departments': department_data
        })

    print(gender_data)

    customer = []
    try:
        customer = Customer.objects.get(user_id=current_user.id)
    except:
        pass
    
    qty = 0
    total = 0
    for cart in carts:
        total = total + cart.amount
        qty = qty + cart.qty
    
    params = {
        'customer':customer,
        'products': products,
        'mobiles': mobiles,
        'laptops': laptops,
        'tvs': tvs,
        'headphones': headphones,
        'homeapps': homeapps,
        'kitapps': kitapps,
        'categories':categories,
        'qty':qty,
        'total':total,
        'carts':carts,
        'genders': gender_data, 
    }

    return render(request, 'index.html', params)



from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Customer, Order, OrderProduct, Cart
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string

@login_required(login_url='/login')
def checkout(request):
    currentuser = request.user
    carts = Cart.objects.filter(user_id=currentuser.id)
    customer = Customer.objects.get(user_id=currentuser.id)
    myuser = User.objects.get(id=currentuser.id)

    total = 0
    qty = 0
    for cart in carts:
        total += cart.amount
        qty += cart.qty

    discount = 10 / 100 * total
    if discount > 20000:
        discount = 20000

    grand_total = total - discount

    # Инициализируем order значением None, чтобы избежать ошибки

    details = {
        'myuser': myuser,
        'customer': customer,
        'carts': carts,
        'qty': qty,
        'total': total,
        'discount': discount,
        'grand_total': grand_total,
    }

    return render(request, 'checkout.html', details)
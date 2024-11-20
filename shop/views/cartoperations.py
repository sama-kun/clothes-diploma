from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Cart, Product, Size
from django.http.response import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

# @require_POST
@login_required(login_url='/login')
def addtocart(request, prid, sizeId):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    check_product = Cart.objects.filter(user_id=current_user.id, product_id=prid, size__size_label=sizeId)
    if check_product.exists():
        data = check_product.first()
        data.qty += 1
        data.save()
    else:
        product = get_object_or_404(Product, id=prid)
        size = get_object_or_404(Size, size_label=sizeId)
        data = Cart()
        data.user = current_user
        data.product = product
        data.qty = 1
        data.size = size
        data.save()
    current_user = request.user
    messages.success(request, data.product.product_name + " added to the Cart.")
    return HttpResponseRedirect(url)

def deletefromcart(request, prid, sizeId):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Cart.objects.get(user_id=current_user.id, product_id=prid, size__size_label = sizeId)
        
    if product.qty == 1:
        product.delete()
    else:
        product.qty = product.qty - 1
        product.save()
    
    messages.success(request, product.product.product_name + " deleted from the Cart.")
    return HttpResponseRedirect(url)

def deleteallfromcart(request, prid, sizeId):
    current_user = request.user
    Cart.objects.get(product_id=prid, user_id=current_user.id, size__size_label=sizeId).delete()
    return HttpResponseRedirect('/cart')

def clearcart(request):
    current_user = request.user
    Cart.objects.filter(user_id=current_user.id).delete()
    return HttpResponseRedirect('/cart')

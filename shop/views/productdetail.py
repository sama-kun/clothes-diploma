from django.shortcuts import render
from shop.models import Customer, Product, Review, Cart, Wishlist

from django.shortcuts import render
from shop.models import Customer, Product, Review, Cart, Wishlist

def productdetail(request, prid):
    current_user = request.user
    product = Product.objects.get(id=prid)
    reviews = Review.objects.filter(product_id=prid)
    carts = Cart.objects.filter(user_id=current_user.id, product_id=prid)
    wishlist = Wishlist.objects.filter(user_id=current_user.id, product_id=prid)

    # Fetch customer data, if available
    customer = []
    try:
        customer = Customer.objects.get(user_id=current_user.id)
    except:
        pass

    # Fetch the quantity of the product in the user's cart
    try:
        pr_qty = Cart.objects.get(user_id=current_user.id, product_id=prid)
        pr_qty = pr_qty.qty
    except:
        pr_qty = 0

    # Calculate the average rating of the product
    no_of_reviews = len(reviews)
    rating = 0
    for review in reviews:
        rating = rating + review.rating
    try:
        rating = rating/no_of_reviews
    except:
        pass

    # Split the product description into multiple parts based on '#'
    desc = product.description
    descs = list(desc.split("#"))

    # Calculate the total quantity and amount from the user's cart
    qty = 0
    total = 0
    for cart in carts:
        total = total + cart.amount
        qty = qty + cart.qty

    # Get Cart items for each size and add quantity to the size object
    sizes_with_qty = []
    for size in product.sizes.all():
        # Find all carts with this product and size
        carts_for_size = carts.filter(size=size)
        size_qty = sum(cart.qty for cart in carts_for_size)  # Total quantity for this size
        
        # Add quantity to the size object
        size_data = {
            'size': size,
            'quantity': size_qty
        }
        sizes_with_qty.append(size_data)

    # Prepare the context to be passed to the template
    details = {
        'customer': customer,
        'product': product,
        'descs': descs,
        'reviews': reviews,
        'no_of_reviews': no_of_reviews,
        'rating': rating,
        'qty': qty,
        'total': total,
        'carts': carts,
        'wishlist': wishlist,
        'pr_qty': pr_qty,
        'sizes': sizes_with_qty,  # Pass sizes with quantity data
    }
    
    return render(request, 'productdetail.html', details)
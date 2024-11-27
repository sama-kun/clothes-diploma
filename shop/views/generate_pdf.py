from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from shop.models import Cart, Order, OrderProduct
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
import asyncio

# Mark the view as asynchronous
async def generate_pdf(request):
    try:
        # Fetch the order and associated products
        carts = Cart.objects.filter(user=request.user)  # Пример, адаптируйте под свою логику
        total = sum(cart.amount for cart in carts)  # Суммарная стоимость
        discount = total * 0.1  # Пример скидки 10%
        grand_total = total - discount
        code = "OD-" + get_random_string(10).upper()
        currentuser = request.user

        # Create order
        order = Order(
            user_id=currentuser.id,
            first_name='Sama',
            last_name='Sama',
            phone=34534534,
            house_no='khgh',
            street='rkgfbs',
            city='jhgjhg',
            pin=654,
            state='jkhgjh',
            total=grand_total,
            code=code,
        )
        order.save()

        # Save order products
        for cart in carts:
            orderpr = OrderProduct(
                order_id=order.id,
                user_id=currentuser.id,
                product_id=cart.product_id,
                qty=cart.qty,
                price=cart.product.price,
                amount=cart.amount,
            )
            orderpr.save()

        Cart.objects.filter(user_id=currentuser.id).delete()
        messages.success(request, "Order has been placed. Thank You 😊")

        # Fetch the order again
        order = Order.objects.get(id=order.id, user=request.user)
        order_products = OrderProduct.objects.filter(order=order)

        # Context data for rendering the PDF
        context = {
            'order': order,
            'order_products': order_products,
        }

        # Render the HTML template
        html_string = render_to_string('order_receipt.html', context)

        # Generate PDF from HTML string
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="order_{order.code}.pdf"'

        # Use xhtml2pdf to create the PDF
        pisa_status = await asyncio.to_thread(pisa.CreatePDF, html_string, dest=response)

        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)

        return response

    except Order.DoesNotExist:
        return HttpResponse("Order not found", status=404)
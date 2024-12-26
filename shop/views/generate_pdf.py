from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils.crypto import get_random_string

from shop.models import Cart, Order, OrderProduct

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import os

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.lib import colors

def generate_pdf(request):
    if request.method == "POST":
        try:
            # Fetch order and products as before
            carts = Cart.objects.filter(user=request.user)
            total = sum(cart.amount for cart in carts)
            discount = total * 0.1
            grand_total = total - discount
            code = "OD-" + get_random_string(10).upper()
            currentuser = request.user

            # Create and save the order, use the request.user data
            order = Order(
                user_id=currentuser.id,
                first_name=request.POST.get('firstname', currentuser.first_name),  # Use request.user if no first name is provided
                last_name=request.POST.get('lastname', currentuser.last_name),  # Use request.user if no last name is provided
                # phone=request.POST.get('phone', currentuser.phone),  # Assuming profile model has phone number
                phone=request.POST.get('phone', 282823),  # Assuming profile model has phone number
                house_no=request.POST.get('house_no', ''),
                street=request.POST.get('street', ''),
                city=request.POST.get('city', ''),
                pin=request.POST.get('pin', 1234),
                state=request.POST.get('state', ''),
                total=grand_total,
                code=code,
            )
            order.save()

            # Save order products
            order_products = []
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
                order_products.append(orderpr)

            # Clear the cart
            Cart.objects.filter(user_id=currentuser.id).delete()

            # Generate the PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Title and header
            p.setFont("Helvetica-Bold", 18)
            p.drawString(200, 750, "Order Receipt")

            p.setFont("Helvetica", 12)
            p.drawString(100, 730, f"Order ID: {order.code}")
            p.drawString(100, 710, f"Name: {order.first_name} {order.last_name}")
            p.drawString(100, 690, f"Phone: {order.phone}")
            p.drawString(100, 670, f"Address: {order.house_no}, {order.street}, {order.city}, {order.state}, {order.pin}")
            
            # Draw a line to separate the address from the products list
            p.setStrokeColor(colors.grey)
            p.line(50, 650, 550, 650)

            # Add table header
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, 630, "Product")
            p.drawString(300, 630, "Quantity")
            p.drawString(400, 630, "Price")
            p.drawString(500, 630, "Total")

            # Add products to the PDF
            y_position = 610
            p.setFont("Helvetica", 10)
            for product in order_products:
                p.drawString(100, y_position, product.product.product_name)
                p.drawString(300, y_position, str(product.qty))
                p.drawString(400, y_position, f"${product.price:.2f}")
                p.drawString(500, y_position, f"${product.amount:.2f}")
                y_position -= 20

            # Add another line to separate products list from summary
            p.setStrokeColor(colors.grey)
            p.line(50, y_position, 550, y_position)

            # Order summary
            y_position -= 20
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y_position, f"Subtotal:  ₸{total:.2f}")
            y_position -= 20
            # p.setFont("Helvetica", 12)
            # p.drawString(100, y_position, f"Discount (10%): -${discount:.2f}")
            y_position -= 20
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y_position, f"Grand Total:  ₸{grand_total:.2f}")

            # Finish PDF generation
            p.showPage()
            p.save()

            buffer.seek(0)
            response.write(buffer.read())
            return response


        except Exception as e:
            # Handle exceptions
            return HttpResponse(f"Error: {e}")
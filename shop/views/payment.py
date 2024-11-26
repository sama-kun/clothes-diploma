import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Устанавливаем секретный ключ Stripe
stripe.api_key = 'sk_test_51MiaNMF9AyD8ZSBFxMOsSo1hMK3qjj8YGOZ994EBAnH9vF1O9yzMdiEsWJqmOdGPlM1YObNfMgLMRofsZ5aDDj8h00GLqebIlJ'

@csrf_exempt
def create_payment(request):
    if request.method == "POST":
        try:
            # Сумма платежа в минимальных единицах валюты (например, 1000 = 10.00 KZT)
            amount = 1000  
            currency = "kzt"  # Валюта платежа

            # Создание PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=["card"],  # Указываем метод оплаты
            )
            print({"clientSecret": intent["client_secret"]})
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

# payments/views.py
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.jwt_check import CookieJWTAuthentication
from store.models import Product
from accounts.models import User
from .models import RazorpayPayment
from .serializers import PaymentSerializer


class CreateOrderAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        user = request.user

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_order = client.order.create({
            "amount": int(product.price * 100),   # amount in paise
            "currency": "INR",
            "payment_capture": 1
        })

        # Save payment record
        payment = RazorpayPayment.objects.create(
            order_id=razorpay_order['id'],
            amount=product.price,
            product=product,
            user=user,
            status='created'
        )

        data = {
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": int(product.price * 100),
            "currency": "INR",
            "payment": PaymentSerializer(payment).data
        }

        return Response(data, status=status.HTTP_201_CREATED)


class VerifyPaymentAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id   = request.data.get('razorpay_order_id')
        razorpay_signature  = request.data.get('razorpay_signature')

        if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
            return Response({"error": "Missing payment details"}, status=status.HTTP_400_BAD_REQUEST)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Verify signature
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        # Update payment record
        try:
            payment = RazorpayPayment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.signature = razorpay_signature
            payment.status = "success"
            payment.save()
        except RazorpayPayment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "message": "Payment verified successfully",
            "payment": PaymentSerializer(payment).data
        }, status=status.HTTP_200_OK)
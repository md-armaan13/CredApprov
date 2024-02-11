"""
Views for the customer API's

"""
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from core.models import Customer
from customer.serializers import CustomerSerializer
from rest_framework.views import exception_handler
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomerView(GenericAPIView):
    '''  
    API to register a new customer
    '''
    serializer_class = CustomerSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone_number'],
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                'monthly_salary': openapi.Schema(type=openapi.TYPE_INTEGER),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                # Add other properties here as needed
            }
        ),
        responses={
            201: "Created",
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):

        phone_number = request.data.get('phone_number')
        if Customer.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({"error": "A user with this phone number already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("hello")
            handled_exception = exception_handler(e, None)
            if handled_exception is not None:
                return handled_exception
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

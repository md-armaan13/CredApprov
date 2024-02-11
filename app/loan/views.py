"""
Views for the Loan API's

"""
from django.http import JsonResponse
from core.models import Loan, Customer
from .serializers import CustomerEligibilitySerializer, CustomerEligibilityResponseSerializer, \
    LoanCreateSerializer, LoanViewSerializer, CustomerLoanSerializer
from rest_framework.views import APIView, exception_handler
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def calculate_credit_score(customer, loans):
    """
    Calculate the credit score of the customer based on the parameters
    """
    credit_score = 100
    total_loan_approved_volume = 0
    current_year = 2023
    current_date = timezone.now()
    total_active_loans_amount = 0

    # 1)  Parameter = No of loans taken in past
    # weight of the paramter is 5%
    No_of_loans_in_past = len(loans)
    credit_score -= (No_of_loans_in_past * 5.0)

    # 2)  Parameter = Loan activity in current year with weightage of 10%

    current_year_loans = [
        loan for loan in loans if loan.date_of_approval.year == current_year]
    credit_score -= (len(current_year_loans) * 10)

    for loan in loans:
        # 3)  Parameter = No of EMI paid on time with weightage of 5%
        # Now We assume that the permissible_no_of_emi is 80% of the tenure
        # if the customer has paid less than 80% of the EMI on time then we will reduce the credit score by 5
        permissible_no_of_emi = loan.tenure * 0.8
        if loan.emi_paid_on_time < permissible_no_of_emi:
            credit_score -= 5

    # 4)  Parameter = Total loan approved volume with weightage of 42%
        total_loan_approved_volume += loan.loan_amount
    # if the total loan approved volume is greater than 50% more than of the Approved Limit of Customer then we will reduce the credit score by 4
    if total_loan_approved_volume > (customer.approved_limit + customer.approved_limit * 0.5):
        credit_score -= 10

    # 5)  Parameter = Sum of active loans amount
    # if the customer has active loans whose end date is greater than the current date
    no_of_active_loans = [
        loan for loan in loans if loan.end_date > current_date]

    for loan in no_of_active_loans:
        total_active_loans_amount += loan.loan_amount
    # if the total active loans amount is greater than the approved limit of customer
    # then we will reduce the credit score to 0
    if total_active_loans_amount > customer.approved_limit:
        credit_score = 0

    print("credit_score", credit_score)
    return credit_score


def check_eligibility_of_customer(credit_score, customer, loans, interest_rate, loan_amount, tenure):
    """
    Check the eligibility of the customer for the loan based on the credit score

    """
    message = ''
    # Checking Eligibility based on Credit Score
    corrected_interest_rate = interest_rate
    if credit_score > 50:
        approval = True
        message = 'Loan approved'
    if credit_score < 50 and credit_score > 30:
        approval = True
        corrected_interest_rate = 13
        message = 'Loan approved with changed interest rate'
    if credit_score < 30 and credit_score > 10:
        approval = True
        corrected_interest_rate = 18
        message = 'Loan approved with changed interest rate'
    if credit_score < 10:
        approval = False
        message = 'Loan not approved due to low credit score'

    current_date = timezone.now()
    # sum of EMI of Current Active Loans
    total_sum_of_current_emi = 0
    no_of_active_loans = [
        loan for loan in loans if loan.end_date > current_date]
    for loan in no_of_active_loans:
        total_sum_of_current_emi += loan.monthly_payment

    if total_sum_of_current_emi > customer.monthly_salary * 0.5:
        approval = False
        message = 'Loan not approved due to high EMI'

    monthly_installment = round(
        (loan_amount * (1 + corrected_interest_rate / 100)) / tenure)

    return (approval, message, corrected_interest_rate, monthly_installment)


class CustomerEligibleView(GenericAPIView):
    '''
    API to check if a customer is eligible for a loan

    '''
    serializer_class = CustomerEligibilitySerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                'loan_amount': openapi.Schema(type=openapi.TYPE_NUMBER, default=30000),
                'interest_rate': openapi.Schema(type=openapi.TYPE_NUMBER, default=5),
                'tenure': openapi.Schema(type=openapi.TYPE_INTEGER, default=33)
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'approval': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'interest_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'tenure': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'corrected_interest_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'monthly_installment': openapi.Schema(type=openapi.TYPE_NUMBER),
                }
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):

        serializer = CustomerEligibilitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        try:
            customer = Customer.objects.get(id=customer_id)
            if loan_amount > customer.approved_limit:
                return JsonResponse({"error": "Loan amount exceeds the approved limit."},
                                    status=status.HTTP_400_BAD_REQUEST)

            loans = Loan.objects.filter(customer_id=customer_id)
            credit_score = calculate_credit_score(customer, loans)

            approval, message, corrected_interest_rate, monthly_installment = check_eligibility_of_customer(
                credit_score, customer, loans, interest_rate, loan_amount, tenure)

            customer_eligibility = {
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "tenure": tenure,
                "corrected_interest_rate": corrected_interest_rate,
                "monthly_installment": monthly_installment
            }

            customer_serializer = CustomerEligibilityResponseSerializer(
                data=customer_eligibility)
            customer_serializer.is_valid(raise_exception=True)
            return JsonResponse(customer_serializer.data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            handled_exception = exception_handler(e, None)
            if handled_exception is not None:
                return handled_exception
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoanCreateView(GenericAPIView):
    """
    API to Create a new loan
    """
    serializer_class = LoanCreateSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['customer_id', 'loan_amount', 'interest_rate', 'tenure'],
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'loan_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                'interest_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                'tenure': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'loan_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'loan_approved': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'monthly_installment': openapi.Schema(type=openapi.TYPE_NUMBER),
                }
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def post(self, request):
        serializer = LoanCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        try:
            customer = Customer.objects.get(id=customer_id)
            if loan_amount > customer.approved_limit:
                return JsonResponse({"error": "Loan amount exceeds the approved limit."},
                                    status=status.HTTP_400_BAD_REQUEST)

            loans = Loan.objects.filter(customer_id=customer_id)
            credit_score = calculate_credit_score(customer, loans)

            approval, message, corrected_interest_rate, monthly_installment = check_eligibility_of_customer(
                credit_score, customer, loans, interest_rate, loan_amount, tenure)

            if not approval:
                response = {
                    "loan_id": None,
                    "customer_id": customer_id,
                    "loan_approved": approval,
                    "message": message,
                    "monthly_installment": monthly_installment
                }

                return JsonResponse(response, status=status.HTTP_200_OK)

            current_date = datetime.now()
            end_date = current_date + relativedelta(months=tenure)

            loan = Loan.objects.create(
                customer_id=customer_id,
                loan_amount=loan_amount,
                interest_rate=corrected_interest_rate,
                tenure=tenure,
                date_of_approval=datetime.now(),
                monthly_payment=monthly_installment,
                emi_paid_on_time=0,
                end_date=end_date
            )

            response = {
                "loan_id": loan.id,
                "customer_id": customer_id,
                "loan_approved": approval,
                "message": message,
                "monthly_installment": monthly_installment
            }

            return JsonResponse(response, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            handled_exception = exception_handler(e, None)
            if handled_exception is not None:
                return handled_exception
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoanDetailView(GenericAPIView):
    """
    API to get the details of a loan
    """
    lookup_field = 'loan_id'
    serializer_class = LoanViewSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'loan_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'interest_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'tenure': openapi.Schema(type=openapi.TYPE_INTEGER),
                    # Add other properties here as needed
                }
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def get(self, request,  loan_id):
        """
        Get the details of a loan
        """
        try:
            loan = Loan.objects.get(id=loan_id)
            loan_serializer = LoanViewSerializer(loan)
            return JsonResponse(loan_serializer.data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return JsonResponse({"error": "Loan does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            handled_exception = exception_handler(e, None)
            if handled_exception is not None:
                return handled_exception
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerLoanDetailView(GenericAPIView):
    '''
    Api to get all the active loans of a customer
    '''
    lookup_field = 'customer_id'
    serializer_class = CustomerLoanSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'loan_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'interest_rate': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'tenure': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'monthly_payment': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'repayments_left': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def get(self, request,  customer_id):
        """
        Get all the Acitve loans of a customer   
        """
        try:
            loans = Loan.objects.filter(customer_id=customer_id)

            current_date = timezone.now()

            # Active Loans
            no_of_active_loans = [
                loan for loan in loans if loan.end_date > current_date]

            for loan in no_of_active_loans:
                # we assume that customer has to pay EMI per months , i.e tenure of loan = Total no of EMI
                # No of Emi left = End_Date_Month - Current_Date_Month
                loan.repayments_left = int((
                    loan.end_date.year - current_date.year) * 12 - (loan.end_date.month - current_date.month))

            loan_serializer = CustomerLoanSerializer(
                no_of_active_loans, many=True)
            return JsonResponse(loan_serializer.data, status=status.HTTP_200_OK, safe=False)

        except Loan.DoesNotExist:
            return JsonResponse({"error": "Loan does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            handled_exception = exception_handler(e, None)
            if handled_exception is not None:
                return handled_exception
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
Models for the core app.

"""
from django.db import models
from django.core.validators import MinValueValidator , RegexValidator
from .validators import validate_not_empty_or_single_space

phone_regex = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits long.",
)
class Customer(models.Model):
    """
    Customer model.
    """

    first_name = models.CharField(max_length=100 , validators=[validate_not_empty_or_single_space])

    last_name = models.CharField(max_length=100 , validators=[validate_not_empty_or_single_space])

    age = models.IntegerField(
        validators=[MinValueValidator(1, message='Age should be positive')])

    phone_number = models.CharField(validators=[phone_regex],max_length=10, unique=True)

    monthly_salary = models.IntegerField(
        validators=[MinValueValidator(0, message='Salary should be positive')])

    approved_limit = models.IntegerField(
        validators=[MinValueValidator(0, message='Salary should be positive')])

    def __str__(self):
        return f'{self.FirstName} {self.LastName}'

    class Meta:
        ordering = ('first_name',)


class Loan(models.Model):
    """
    Loan model.
    """
    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    loan_amount = models.IntegerField(validators=[
        MinValueValidator(1, message='Loan Amount should be positive')])

    tenure = models.IntegerField(validators=[
        MinValueValidator(0, message='Tenure should be positive')])

    interest_rate = models.DecimalField(max_digits=12, decimal_places=2, validators=[
        MinValueValidator(0, message='Interst Rate should be positive')])

    monthly_payment = models.IntegerField(validators=[
        MinValueValidator(0, message='Monthly paymemt should be positive')])

    emi_paid_on_time = models.IntegerField(validators=[
        MinValueValidator(0, message='No of Emi should be positive')])

    date_of_approval = models.DateTimeField(blank=True, null=True)

    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Loan for {self.customer.FirstName} {self.customer.LastName}'




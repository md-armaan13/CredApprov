
from django.db import models
from django.core.validators import MinValueValidator


class Loan(models.Model):
    """
    Loan model.
    """
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)

    loan_amount = models.DecimalField(max_digits=12, validators=[
                                MinValueValidator(0, message='Loan Amount should be positive')])

    tenure = models.IntegerField(max_digits=10, validators=[
                                MinValueValidator(0, message='Tenure should be positive')])

    interest_rate = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(0, message='Interst Rate should be positive')])

    monthly_payment = models.IntegerField(max_digits=12, validators=[
                                MinValueValidator(0, message='Monthly paymemt should be positive')])

    emi_paid_on_time = models.IntegerField(max_digits=8, validators=[
                                MinValueValidator(0, message='No of Emi should be positive')])

    date_of_approval = models.DateTimeField(blank=True, null=True)

    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Loan for {self.customer.FirstName} {self.customer.LastName}'

    class Meta:
        ordering = ('-date',)

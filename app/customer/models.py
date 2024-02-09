
from django.db import models
from django.core.validators import MinValueValidator


class Customer(models.Model):
    """
    Customer model.
    """
    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    age = models.IntegerField(max_digits=6,
                              validators=[MinValueValidator(1, message='Age should be positive')])

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    monthly_salary = models.IntegerField(max_digits=12,
                                        validators=[MinValueValidator(0, message='Salary should be positive')])
    
    approved_limit = models.IntegerField(max_digits=12,
                                        validators=[MinValueValidator(0, message='Salary should be positive')])

    def __str__(self):
        return f'{self.FirstName} {self.LastName}'

    class Meta:
        ordering = ('FirstName',)

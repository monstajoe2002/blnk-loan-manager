from django.db import models
import uuid
from user.models import User


# Create your models here.
class LoanCustomer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    term = models.IntegerField(default=1)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class LoanProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Loan(models.Model):
    class Status(models.TextChoices):
        PENDING = "P", "Pending"
        APPROVED = "A", "Approved"
        REJECTED = "R", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan_customer = models.ForeignKey(LoanCustomer, on_delete=models.CASCADE, null=True)
    loan_provider = models.ForeignKey(LoanProvider, on_delete=models.CASCADE, null=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )


class BankPersonnel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    min_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_duration = models.IntegerField(default=1)  # in months

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        BANK_PERSONNEL = "BP", "Bank Personnel"
        LOAN_PROVIDER = "LP", "Loan Provider"
        LOAN_CUSTOMER = "LC", "Loan Customer"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=2, choices=Role.choices, default=Role.LOAN_CUSTOMER
    )
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ["role", "username", "password"]
    USERNAME_FIELD = "email"

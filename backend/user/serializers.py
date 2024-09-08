from django.db import transaction
from .models import User
from rest_framework import serializers
from loans.models import LoanCustomer, LoanProvider, BankPersonnel, Loan


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        if user.role == User.Role.LOAN_CUSTOMER:
            loan_customer = LoanCustomer.objects.create(user=user)
            Loan.objects.create(
                loan_customer=loan_customer,
                status=Loan.Status.PENDING,
            )
        elif user.role == User.Role.LOAN_PROVIDER:
            loan_provider = LoanProvider.objects.create(user=user)

            Loan.objects.create(loan_provider=loan_provider, status=Loan.Status.PENDING)
        elif user.role == User.Role.BANK_PERSONNEL:
            BankPersonnel.objects.create(user=user)
        else:
            pass
        return user

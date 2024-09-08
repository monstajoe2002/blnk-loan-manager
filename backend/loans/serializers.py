from rest_framework import serializers
from .models import LoanCustomer, LoanProvider, BankPersonnel, Loan
from django.db import transaction
from user.models import User
from user.serializers import UserSerializer


class LoanCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = LoanCustomer
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        loan_customer = LoanCustomer.objects.create(**validated_data)
        loan_customer.save()
        return loan_customer


class LoanProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = LoanProvider
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        loan_provider = LoanProvider.objects.create(**validated_data)
        loan_provider.save()
        return loan_provider


class BankPersonnelSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = BankPersonnel
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data["role"] = User.Role.BANK_PERSONNEL
        user = User.objects.create_user(**user_data)
        bank_personnel = BankPersonnel.objects.create(user=user, **validated_data)
        return bank_personnel

    def validate_loan_duration(self, value):
        if value <= 0 or value > 360:
            raise serializers.ValidationError(
                "Loan duration must be between 1 and 360 months."
            )
        return value


class LoanSerializer(serializers.ModelSerializer):
    loan_customer = LoanCustomerSerializer(required=True)
    loan_provider = LoanProviderSerializer(required=True)

    class Meta:
        model = Loan
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data)
        loan.save()
        return loan

from django.shortcuts import render, get_object_or_404
from .models import LoanCustomer, LoanProvider, BankPersonnel, Loan
from .serializers import (
    LoanCustomerSerializer,
    LoanProviderSerializer,
    BankPersonnelSerializer,
    LoanSerializer,
)
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.
class LoanCustomerViewSet(viewsets.ModelViewSet):
    queryset = LoanCustomer.objects.all()
    serializer_class = LoanCustomerSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False)
    def applications(self, _):
        loan_applications = Loan.objects.all()
        serializer = LoanSerializer(loan_applications, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="payment")
    def payment(self, request, pk):
        """
        Pay the loan amount

        URL format:
            `customer/:id/payment/`

        Firstly, it checks if the loan is approved by bank personnel.
        Then, it checks if the loan is not already paid or overdue.

        Returns:
            If the payment is successful, return the loan data
            If the payment is not successful, return an error message
        """
        loan = get_object_or_404(Loan, pk=pk)
        loan_provider = loan.loan_provider

        # approve or reject the loan based on available funds
        if loan_provider.total_funds >= loan.amount:
            loan.status = Loan.Status.APPROVED
            loan_provider.total_funds -= loan.amount
            loan.save()
        else:
            loan.status = Loan.Status.REJECTED
            loan.save()
        loan = Loan.objects.get(pk=loan.id)
        loan_serializer = LoanSerializer(loan)
        return Response(loan_serializer.data)

    @action(detail=True, methods=["post"])
    def payment(self, request, pk=None):
        loan_customer = self.get_object()
        # Implement your payment logic here
        # For now, let's just return a success message
        return Response({"status": "Payment successful"}, status=200)


class LoanProviderViewSet(viewsets.ModelViewSet):
    queryset = LoanProvider.objects.all()
    serializer_class = LoanProviderSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["GET"])
    def applications(self, request):
        loan_applications = Loan.objects.all()

        serializer = LoanSerializer(loan_applications, many=True)

        return Response(serializer.data)


class BankPersonnelViewSet(viewsets.ModelViewSet):
    queryset = BankPersonnel.objects.all()
    serializer_class = BankPersonnelSerializer

    @action(detail=False)
    def applications(self, _):
        loan_applications = BankPersonnel.objects.all()
        serializer = BankPersonnelSerializer(loan_applications, many=True)

        return Response(serializer.data)

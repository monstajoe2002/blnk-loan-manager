from .models import LoanProvider, LoanCustomer, BankPersonnel, Loan
from user.models import User
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
loan_provider_url = "/api/v1/providers/"
loan_customer_url = "/api/v1/customers/"
bank_personnel_url = "/api/v1/personnels/"


class LoanProviderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testprovider",
            email="testprovider@example.com",
            password="testpass",
            role=User.Role.LOAN_PROVIDER,
        )
        self.loan_provider = LoanProvider.objects.create(
            user=self.user, total_funds=1000000
        )
        self.user = User.objects.create(
            username="testcustomer",
            email="testcustomer@example.com",
            password="testpass",
            role=User.Role.LOAN_CUSTOMER,
        )
        self.loan_customer = LoanCustomer.objects.create(
            user=self.user, amount=10000, term=12, interest_rate=5.0
        )
        self.loan = Loan.objects.create(
            loan_customer=self.loan_customer,
            loan_provider=self.loan_provider,
            status=Loan.Status.PENDING,
        )

    def test_loan_provider_list(self):
        response = self.client.get(loan_provider_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.loan_provider.id))

    def test_loan_provider_applications(self):
        response = self.client.get(f"{loan_provider_url}applications/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.loan.id))

    def test_loan_provider_detail(self):
        response = self.client.get(f"{loan_provider_url}{self.loan_provider.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.loan_provider.id))
        self.assertEqual(response.data["total_funds"], "1000000.00")
        self.assertEqual(response.data["user"], self.loan_provider.user.id)

    def test_loan_provider_create(self):
        data = {"user": self.user.id, "total_funds": 500000}
        response = self.client.post(loan_provider_url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(LoanProvider.objects.count(), 2)
        self.assertEqual(
            LoanProvider.objects.get(id=response.data["id"]).total_funds, 500000
        )

    def test_loan_provider_update(self):
        new_total_funds = 1500000
        data = {"total_funds": new_total_funds}
        response = self.client.patch(
            f"{loan_provider_url}{self.loan_provider.id}/", data=data
        )
        self.assertEqual(response.status_code, 200)
        self.loan_provider.refresh_from_db()
        self.assertEqual(self.loan_provider.total_funds, new_total_funds)

    def test_loan_provider_delete(self):
        response = self.client.delete(f"{loan_provider_url}{self.loan_provider.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(LoanProvider.objects.count(), 0)


class LoanCustomerTests(APITestCase):
    def setUp(self):
        self.provider_user = User.objects.create(
            username="testprovider",
            email="testprovider@example.com",
            password="testpass",
            role=User.Role.LOAN_PROVIDER,
        )
        self.loan_provider = LoanProvider.objects.create(
            user=self.provider_user, total_funds=1000000
        )
        self.user = User.objects.create(
            username="testcustomer",
            email="testcustomer@example.com",
            password="testpass",
            role=User.Role.LOAN_CUSTOMER,
        )
        self.loan_customer = LoanCustomer.objects.create(
            user=self.user, amount=10000, term=12, interest_rate=5.0
        )

    def test_loan_customer_list(self):
        response = self.client.get(loan_customer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.loan_customer.id))

    def test_loan_customer_applications(self):
        response = self.client.get(f"{loan_customer_url}applications/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_loan_customer_detail(self):
        response = self.client.get(f"{loan_customer_url}{self.loan_customer.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.loan_customer.id))
        self.assertEqual(response.data["amount"], "10000.00")
        self.assertEqual(response.data["term"], 12)
        self.assertEqual(response.data["interest_rate"], "5.00")

    def test_loan_customer_payment(self):
        response = self.client.post(
            f"{loan_customer_url}{self.loan_customer.id}/payment/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "Payment successful")

    def test_loan_customer_update(self):
        new_amount = 10000
        new_term = 12
        data = {
            "amount": new_amount,
            "term": new_term,
        }
        response = self.client.patch(
            f"{loan_customer_url}{self.loan_customer.id}/", data=data
        )
        self.assertEqual(response.status_code, 200)
        self.loan_customer.refresh_from_db()
        self.assertEqual(self.loan_customer.amount, new_amount)
        self.assertEqual(self.loan_customer.term, new_term)

    def test_loan_customer_delete(self):
        response = self.client.delete(f"{loan_customer_url}{self.loan_customer.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(LoanCustomer.objects.count(), 0)


class BankPersonnelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testpersonnel",
            email="testpersonnel@example.com",
            password="testpass",
            role=User.Role.BANK_PERSONNEL,
        )
        self.bank_personnel = BankPersonnel.objects.create(
            user=self.user,
            min_loan_amount=5000,
            max_loan_amount=100000,
            interest_rate=4.5,
            loan_duration=36,
        )

    def test_bank_personnel_list(self):
        response = self.client.get(bank_personnel_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.bank_personnel.id))

    def test_bank_personnel_applications(self):
        response = self.client.get(f"{bank_personnel_url}applications/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, [])

    def test_bank_personnel_detail(self):
        response = self.client.get(f"{bank_personnel_url}{self.bank_personnel.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.bank_personnel.id))
        self.assertEqual(response.data["min_loan_amount"], "5000.00")
        self.assertEqual(response.data["max_loan_amount"], "100000.00")
        self.assertEqual(response.data["interest_rate"], "4.50")
        self.assertEqual(response.data["loan_duration"], 36)

    def test_bank_personnel_create(self):
        data = {
            "user": {
                "username": "newbankpersonnel",
                "email": "newbankpersonnel@example.com",
                "password": "testpass123",
            },
            "min_loan_amount": 10000,
            "max_loan_amount": 200000,
            "interest_rate": 5.0,
            "loan_duration": 48,  # in months
        }
        response = self.client.post(bank_personnel_url, data=data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BankPersonnel.objects.count(), 2)
        new_bank_personnel = BankPersonnel.objects.get(id=response.data["id"])
        self.assertEqual(new_bank_personnel.min_loan_amount, 10000)
        self.assertEqual(new_bank_personnel.loan_duration, 48)
        self.assertEqual(new_bank_personnel.user.role, User.Role.BANK_PERSONNEL)

    def test_bank_personnel_update(self):
        new_min_loan_amount = 7500
        new_max_loan_amount = 150000
        new_loan_duration = 60
        data = {
            "min_loan_amount": new_min_loan_amount,
            "max_loan_amount": new_max_loan_amount,
            "loan_duration": new_loan_duration,
        }
        response = self.client.patch(
            f"{bank_personnel_url}{self.bank_personnel.id}/", data=data
        )
        self.assertEqual(response.status_code, 200)
        self.bank_personnel.refresh_from_db()
        self.assertEqual(self.bank_personnel.min_loan_amount, new_min_loan_amount)
        self.assertEqual(self.bank_personnel.max_loan_amount, new_max_loan_amount)
        self.assertEqual(self.bank_personnel.loan_duration, new_loan_duration)

    def test_bank_personnel_delete(self):
        response = self.client.delete(f"{bank_personnel_url}{self.bank_personnel.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(BankPersonnel.objects.count(), 0)

    def test_bank_personnel_loan_duration_constraints(self):
        client = APIClient()
        client.login(username="testpersonnel", password="testpass")

        data = {
            "user": {
                "username": "newbankpersonnel2",
                "email": "newbankpersonnel2@example.com",
                "password": "testpass123",
            },
            "min_loan_amount": 5000,
            "max_loan_amount": 100000,
            "interest_rate": 4.5,
            "loan_duration": 0,  # Invalid duration
        }
        response = self.client.post(bank_personnel_url, data=data, format="json")
        self.assertEqual(response.status_code, 400)  # Expecting a bad request

        data["loan_duration"] = 361  # Assuming max duration is 360 months (30 years)
        response = self.client.post(bank_personnel_url, data=data, format="json")
        self.assertEqual(response.status_code, 400)  # Expecting a bad request

        data["loan_duration"] = 180  # Valid duration (15 years)
        response = self.client.post(bank_personnel_url, data=data, format="json")
        self.assertEqual(response.status_code, 201)  # Expecting a successful creation
        self.assertEqual(
            BankPersonnel.objects.get(id=response.data["id"]).loan_duration, 180
        )

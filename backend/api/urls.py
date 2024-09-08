from django.urls import include, path
from rest_framework import routers

from user.views import UserViewSet
from loans.views import (
    LoanCustomerViewSet,
    LoanProviderViewSet,
    BankPersonnelViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"providers", LoanProviderViewSet)
router.register(r"customers", LoanCustomerViewSet)
router.register(r"personnels", BankPersonnelViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

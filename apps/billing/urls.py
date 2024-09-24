from django.urls import path
from .views.BillingView import BillView, BillDetailView, AdminAggregationView

urlpatterns = [
    path('user/', BillView.as_view(), name='user-bill-list'),  # GET, POST
    path('user/<int:bill_id>/', BillDetailView.as_view(), name='user-bill-detail'),  # GET, PUT, DELETE
    path('admin/aggregate/', AdminAggregationView.as_view(), name='admin-billing-aggregate'),  # GET
]

from django.urls import path
from .views.ConsumptionView import ConsumptionView
from .views.ConsumptionView import ConsumptionView, AdminAggregationView, AdminUserAggregationView

urlpatterns = [
    path('user/', ConsumptionView.as_view(), name='user-consumption'),  # User-specific consumption endpoints
        path('admin/aggregate/', AdminAggregationView.as_view(), name='admin-consumption-aggregate'),  # Admin: aggregate for all users
    path('admin/aggregate/user/<int:user_id>/', AdminUserAggregationView.as_view(), name='admin-user-consumption-aggregate'),  # Admin: aggregate for a specific user
]

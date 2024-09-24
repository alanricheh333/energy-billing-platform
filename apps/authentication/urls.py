from django.urls import path
from .views.UserViews import RegisterView, AdminRegisterView, LoginView, UserProfileView, AdminUserManagementView # type: ignore

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('admin/user/<int:user_id>/', AdminUserManagementView.as_view(), name='admin-user-management'),
]

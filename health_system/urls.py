from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.admin import custom_admin_site  # Import the custom admin site
from django.contrib.auth.views import LogoutView
from django.views.decorators.http import require_GET
from django.shortcuts import redirect  # Add this import
from django.contrib.auth import logout  # Add this import
from core import views  # Import the entire views module
from core.views import root_redirect  # Import root_redirect explicitly
from core.forms import CustomPasswordResetForm, CustomSetPasswordForm  # Import the custom forms


@require_GET
def custom_logout(request):
    logout(request)
    return redirect('login')
    
urlpatterns = [
    path('', root_redirect),  # This will always redirect to login
    path('admin/', custom_admin_site.urls),  # Use the custom admin site
    path('login/', views.user_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        form_class=CustomPasswordResetForm
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    path('', include('core.urls')),
]
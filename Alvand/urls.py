from django.urls import path, re_path
from . import views, views_improved
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('dashboard/', views.dashboardPage.as_view(), name='dashboard'),
    path('dashboard/export/', views.dashboard_export, name='dashboard_export'),
    path('api/live-call-status/', views.live_call_status, name='live_call_status'),
    path('dashboard-improved/', views_improved.ImprovedDashboardView.as_view(), name='dashboard-improved'),
    path('smdr-dashboard/', views_improved.SMDRDashboardView.as_view(), name='smdr-dashboard'),
    path('settings/', views.systemSettings.as_view(), name='settings'),
    path('support/', views.support, name='support'),
    path('errors/', views.errorsPage.as_view(), name='errors'),
    path('errors/export/', views.error_export, name='error_export'),
    path('errors/search/', views.error_search_ajax, name='error_search_ajax'),
    path('user/', views.UserForm.as_view(), name='user'),
    path('get-user-data/', views.get_user_data, name='get_user_data'),
    path('get-cable-types/', views.get_cable_types, name='get_cable_types'),
    path('userprofile/', views.userprofile_view, name='userprofile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('', views.userLogin.as_view(), name='index'),
    path('login/', views.userLogin.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('license/', views.licenseNotActive, name='license'),
    path('test-user-create/', views.test_user_create, name='test_user_create'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

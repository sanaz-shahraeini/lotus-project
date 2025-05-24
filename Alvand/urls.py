from django.urls import path, re_path
from . import views, views_improved
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView


urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('dashboard/', views.dashboardPage.as_view(), name='dashboard'),
    path('dashboard-improved/', views_improved.ImprovedDashboardView.as_view(), name='dashboard-improved'),
    path('smdr-dashboard/', views_improved.SMDRDashboardView.as_view(), name='smdr-dashboard'),
    path('settings/', views.systemSettings.as_view(), name='settings'),
    path('support/', views.support, name='support'),
    path('errors/', views.errorsPage.as_view(), name='errors'),
    path('user/', views.UserForm.as_view(), name='user'),
    path('', views.userLogin.as_view(), name='index'),
    path('login/', views.userLogin.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('license/', views.licenseNotActive, name='license'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

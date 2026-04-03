from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]   
urlpatterns = format_suffix_patterns(urlpatterns)
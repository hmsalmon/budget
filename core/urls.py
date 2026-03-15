from django.urls import path
from . import views

urlpatterns = [
    path('edit', views.edit, name='edit'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('overview', views.overview, name='overview'),
    path('scheduled', views.scheduled, name="scheduled"),
    path('transaction/<int:pk>/update', views.transaction_update, name='transaction_update')
]


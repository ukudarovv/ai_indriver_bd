from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('list/', views.list_plates, name='list_plates'),
    path('check/<str:plate>/', views.check_plate, name='check_plate'),
]

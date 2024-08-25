from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("payment", views.payment, name="payment"),
    path("ordersuccess", views.success, name="success"),
    path('get-animals/<int:category_id>/', views.get_animals, name='get_animals'),
]
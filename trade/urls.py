from django.urls import path
from . import views

app_name = 'trade'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/sync/', views.OrderSyncView.as_view(), name='order_sync'),
] 
from django.urls import path
from . import views

app_name = 'trade'

urlpatterns = [
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views.OrderEditView.as_view(), name='order_edit'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product_detail_api'),
] 
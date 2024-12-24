from django.urls import path
from . import views

app_name = 'storage'

urlpatterns = [
    path('stock/', views.StockListView.as_view(), name='stock_list'),
    path('sync/', views.StockSyncView.as_view(), name='stock_sync'),
] 
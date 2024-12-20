from django.urls import path
from . import views

app_name = 'storage'

urlpatterns = [
    path('', views.StockListView.as_view(), name='stock_list'),
] 
from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    SPUListView, SPUCreateView, SPUUpdateView, SPUDeleteView,
    SKUListView, SKUCreateView, SKUUpdateView, SKUDeleteView
)

app_name = 'gallery'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('spus/', SPUListView.as_view(), name='spu_list'),
    path('spus/add/', SPUCreateView.as_view(), name='spu_add'),
    path('spus/<int:pk>/edit/', SPUUpdateView.as_view(), name='spu_edit'),
    path('spus/<int:pk>/delete/', SPUDeleteView.as_view(), name='spu_delete'),
    path('skus/', SKUListView.as_view(), name='sku_list'),
    path('skus/add/', SKUCreateView.as_view(), name='sku_add'),
    path('skus/<int:pk>/edit/', SKUUpdateView.as_view(), name='sku_edit'),
    path('skus/<int:pk>/delete/', SKUDeleteView.as_view(), name='sku_delete'),
] 
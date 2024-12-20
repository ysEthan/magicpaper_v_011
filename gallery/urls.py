from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    SPUListView, SPUCreateView, SPUUpdateView, SPUDeleteView
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
] 
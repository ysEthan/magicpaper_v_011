from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Stock, Warehouse

class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'storage/stock_list.html'
    context_object_name = 'stocks'
    paginate_by = 10
    login_url = '/muggle/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        warehouse_id = self.request.GET.get('warehouse')
        
        if search_query:
            queryset = queryset.filter(
                sku__sku_code__icontains=search_query
            )
        
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
            
        return queryset.select_related('warehouse', 'sku', 'sku__spu')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'stock'
        context['warehouses'] = Warehouse.objects.all()
        context['selected_warehouse'] = self.request.GET.get('warehouse', '')
        return context

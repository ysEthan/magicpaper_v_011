from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Stock, Warehouse
from gallery.models import SPU
from . import sync
import logging

logger = logging.getLogger(__name__)

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
        product_type = self.request.GET.get('product_type')
        
        if search_query:
            queryset = queryset.filter(
                sku__sku_code__icontains=search_query
            )
        
        if warehouse_id:
            queryset = queryset.filter(warehouse_id=warehouse_id)
            
        if product_type:
            queryset = queryset.filter(sku__spu__product_type=product_type)
            
        return queryset.select_related('warehouse', 'sku', 'sku__spu')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'stock'
        context['warehouses'] = Warehouse.objects.all()
        context['selected_warehouse'] = self.request.GET.get('warehouse', '')
        
        # 添加产品类型数据
        product_types = []
        for pt in SPU.PRODUCT_TYPE_CHOICES:
            count = SPU.objects.filter(product_type=pt[0]).count()
            if count > 0:  # 只显示有数据的类型
                product_types.append({
                    'value': pt[0],
                    'label': pt[1],
                    'count': count
                })
        context['product_types'] = product_types
        context['selected_product_type'] = self.request.GET.get('product_type', '')
        
        return context

class StockSyncView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            sync.sync_all_stock()
            messages.success(request, '库存数据同步成功！')
            logger.info(f"用户 {request.user.username} 同步库存数据成功")
        except Exception as e:
            error_msg = f'同步失败：{str(e)}'
            messages.error(request, error_msg)
            logger.error(f"用户 {request.user.username} 同步库存数据失败: {str(e)}")
        return redirect('storage:stock_list')

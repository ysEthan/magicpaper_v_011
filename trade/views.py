from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Order, Shop
from gallery.models import SKU
from . import sync
import logging
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.edit import BaseDeleteView
from django.db.models import Q

logger = logging.getLogger(__name__)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'trade/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    login_url = '/muggle/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        shop_id = self.request.GET.get('shop')
        status = self.request.GET.get('status')
        
        if search_query:
            queryset = queryset.filter(
                order_no__icontains=search_query
            ) | queryset.filter(
                platform_order_no__icontains=search_query
            ) | queryset.filter(
                recipient_name__icontains=search_query
            )
        
        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)
            
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset.select_related('shop')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'order'
        context['shops'] = Shop.objects.filter(is_active=True)
        context['selected_shop'] = self.request.GET.get('shop', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['status_choices'] = Order.OrderStatus.choices
        return context

class OrderSyncView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            success, message = sync.sync_all_trade()
            if success:
                messages.success(request, '订单数据同步成功！')
                logger.info(f"用户 {request.user.username} 同步订单数据成功")
            else:
                messages.error(request, f'同步失败：{message}')
                logger.error(f"用户 {request.user.username} 同步订单数据失败: {message}")
        except Exception as e:
            error_msg = f'同步失败：{str(e)}'
            messages.error(request, error_msg)
            logger.error(f"用户 {request.user.username} 同步订单数据失败: {str(e)}")
        return redirect('trade:order_list')
    def get(self, request, *args, **kwargs):
        try:
            success, message = sync.sync_all_trade()
            if success:
                messages.success(request, '订单数据同步成功！')
                logger.info(f"用户 {request.user.username} 同步订单数据成功")
            else:
                messages.error(request, f'同步失败：{message}')
                logger.error(f"用户 {request.user.username} 同步订单数据失败: {message}")
        except Exception as e:
            error_msg = f'同步失败：{str(e)}'
            messages.error(request, error_msg)
            logger.error(f"用户 {request.user.username} 同步订单数据失败: {str(e)}")
        return redirect('trade:order_list')

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'trade/order_form.html'
    fields = ['shop', 'platform_order_no', 'recipient_name', 'recipient_country', 'recipient_state', 
              'recipient_city', 'recipient_address', 'paid_amount', 'buyer_remark', 'cs_remark']
    success_url = reverse_lazy('trade:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = SKU.objects.filter(status=1)
        return context

class OrderEditView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'trade/order_form.html'
    fields = ['shop', 'platform_order_no', 'recipient_name', 'recipient_country', 'recipient_state', 
              'recipient_city', 'recipient_address', 'paid_amount', 'buyer_remark', 'cs_remark']
    success_url = reverse_lazy('trade:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = SKU.objects.filter(status=1)
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'trade/order_detail.html'
    context_object_name = 'order'

class OrderDeleteView(LoginRequiredMixin, BaseDeleteView):
    model = Order
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'status': 'success'})

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class ProductDetailAPIView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            sku = SKU.objects.get(pk=pk)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'sku': sku.sku_code,
                    'price': float(sku.stock),  # 暂时使用库存作为价格
                    'name': f"{sku.sku_name} ({sku.sku_code})"
                }
            })
        except SKU.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '商品不存在'
            }, status=404)

class ProductSearchAPIView(LoginRequiredMixin, View):
    def get(self, request):
        sku = request.GET.get('sku', '')
        if not sku:
            return JsonResponse({
                'results': [],
                'pagination': {'more': False}
            })
            
        try:
            product = SKU.objects.get(sku_code=sku, status=1)
            results = [{
                'id': product.id,
                'text': product.sku_name,
                'sku': product.sku_code,
                'price': float(product.stock)  # 暂时使用库存作为价格
            }]
        except SKU.DoesNotExist:
            results = []
        
        return JsonResponse({
            'results': results,
            'pagination': {'more': False}
        })
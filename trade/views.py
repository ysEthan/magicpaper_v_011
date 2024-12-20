from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, Shop

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

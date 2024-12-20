from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category, SPU, SKU
from django.contrib import messages
from .sync import ProductSync

# Create your views here.

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'gallery/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    login_url = '/muggle/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                category_name_zh__icontains=search_query
            ) | queryset.filter(
                category_name_en__icontains=search_query
            )
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'category'  # 用于高亮左侧菜单
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'gallery/category_form.html'
    fields = ['category_name_zh', 'category_name_en', 'description', 'image', 
             'parent', 'rank_id', 'level', 'is_last_level', 'status']
    success_url = reverse_lazy('gallery:category_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新增类目'
        context['active_menu'] = 'category'
        return context

    def form_valid(self, form):
        messages.success(self.request, '类目创建成功！')
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'gallery/category_form.html'
    fields = ['category_name_zh', 'category_name_en', 'description', 'image', 
             'parent', 'rank_id', 'level', 'is_last_level', 'status']
    success_url = reverse_lazy('gallery:category_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '编辑类目'
        context['active_menu'] = 'category'
        return context

    def form_valid(self, form):
        messages.success(self.request, '类目更新成功！')
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('gallery:category_list')
    login_url = '/muggle/login/'
    template_name = 'gallery/category_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '删除类目'
        context['active_menu'] = 'category'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, '类目删除成功！')
        return super().delete(request, *args, **kwargs)

class SPUListView(LoginRequiredMixin, ListView):
    model = SPU
    template_name = 'gallery/spu_list.html'
    context_object_name = 'spus'
    paginate_by = 10
    login_url = '/muggle/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                spu_name__icontains=search_query
            ) | queryset.filter(
                spu_code__icontains=search_query
            )
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'spu'  # 用于高亮左侧菜单
        return context

class SPUCreateView(LoginRequiredMixin, CreateView):
    model = SPU
    template_name = 'gallery/spu_form.html'
    fields = ['spu_code', 'spu_name', 'product_type', 'spu_remark', 
             'sales_channel', 'category', 'status']
    success_url = reverse_lazy('gallery:spu_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新增SPU'
        context['active_menu'] = 'spu'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'SPU创建成功！')
        return super().form_valid(form)

class SPUUpdateView(LoginRequiredMixin, UpdateView):
    model = SPU
    template_name = 'gallery/spu_form.html'
    fields = ['spu_code', 'spu_name', 'product_type', 'spu_remark', 
             'sales_channel', 'category', 'status']
    success_url = reverse_lazy('gallery:spu_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '编辑SPU'
        context['active_menu'] = 'spu'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'SPU更新成功！')
        return super().form_valid(form)

class SPUDeleteView(LoginRequiredMixin, DeleteView):
    model = SPU
    success_url = reverse_lazy('gallery:spu_list')
    login_url = '/muggle/login/'
    template_name = 'gallery/spu_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '删除SPU'
        context['active_menu'] = 'spu'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'SPU删除成功！')
        return super().delete(request, *args, **kwargs)

class SKUListView(LoginRequiredMixin, ListView):
    model = SKU
    template_name = 'gallery/sku_list.html'
    context_object_name = 'skus'
    paginate_by = 10
    login_url = '/muggle/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                sku_name__icontains=search_query
            ) | queryset.filter(
                sku_code__icontains=search_query
            )
        return queryset.select_related('spu')  # 优化查询，减少数据库访问
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'sku'  # 用于高亮左侧菜单
        return context

class SKUCreateView(LoginRequiredMixin, CreateView):
    model = SKU
    template_name = 'gallery/sku_form.html'
    fields = ['sku_code', 'sku_name', 'provider_code', 'plating_process', 
             'color', 'material', 'length', 'width', 'height', 'weight', 
             'status', 'spu', 'img_url']
    success_url = reverse_lazy('gallery:sku_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新增SKU'
        context['active_menu'] = 'sku'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'SKU创建成功！')
        return super().form_valid(form)

class SKUUpdateView(LoginRequiredMixin, UpdateView):
    model = SKU
    template_name = 'gallery/sku_form.html'
    fields = ['sku_code', 'sku_name', 'provider_code', 'plating_process', 
             'color', 'material', 'length', 'width', 'height', 'weight', 
             'status', 'spu', 'img_url']
    success_url = reverse_lazy('gallery:sku_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '编辑SKU'
        context['active_menu'] = 'sku'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'SKU更新成功！')
        return super().form_valid(form)

class SKUDeleteView(LoginRequiredMixin, DeleteView):
    model = SKU
    success_url = reverse_lazy('gallery:sku_list')
    login_url = '/muggle/login/'
    template_name = 'gallery/sku_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '删除SKU'
        context['active_menu'] = 'sku'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'SKU删除成功！')
        return super().delete(request, *args, **kwargs)

class SKUSyncView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            sync = ProductSync()
            count = sync.sync_products()
            sync.clean_old_images()  # 清理旧图片
            messages.success(request, f'成功同步 {count} 条数据！')
        except Exception as e:
            messages.error(request, f'同步失败：{str(e)}')
        return redirect('gallery:sku_list')

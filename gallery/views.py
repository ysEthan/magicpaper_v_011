from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category, SPU, SKU
from django.contrib.auth.models import User
from django.contrib import messages
from .sync import ProductSync
from django.db.models import Q, Count
from django.http import HttpResponseRedirect
from .forms import SKUForm

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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'category'  # 添加 active_submenu
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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'category'  # 添加 active_submenu
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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'category'  # 添加 active_submenu
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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'category'  # 添加 active_submenu
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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'spu'  # 添加 active_submenu
        return context

class SPUCreateView(LoginRequiredMixin, CreateView):
    model = SPU
    template_name = 'gallery/spu_form2.html'
    fields = ['spu_code', 'spu_name', 'product_type', 'spu_remark', 
             'sales_channel', 'category', 'status']
    success_url = reverse_lazy('gallery:spu_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新增SPU'
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'spu'  # 添加 active_submenu
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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'spu'  # 添加 active_submenu
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
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'spu'  # 添加 active_submenu
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
        
        # 获取筛选参数
        search_query = self.request.GET.get('search')
        category_id = self.request.GET.get('category')
        color = self.request.GET.get('color')
        material = self.request.GET.get('material')
        plating = self.request.GET.get('plating')
        product_type = self.request.GET.get('product_type')  # 添加产品类型筛选
        
        # 应用筛选条件
        if search_query:
            queryset = queryset.filter(
                Q(sku_name__icontains=search_query) |
                Q(sku_code__icontains=search_query) |
                Q(spu__spu_code__icontains=search_query) |
                Q(spu__spu_name__icontains=search_query)
            )
        
        if category_id and category_id.isdigit():
            queryset = queryset.filter(spu__category_id=int(category_id))
            
        if color:
            queryset = queryset.filter(color=color)
            
        if material:
            queryset = queryset.filter(material=material)
            
        if plating:
            queryset = queryset.filter(plating_process=plating)
            
        if product_type:  # 添加产品类型筛选条件
            queryset = queryset.filter(spu__product_type=product_type)
        
        return queryset.select_related('spu', 'spu__category')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 基本查询参数
        context['search_query'] = self.request.GET.get('search', '')
        context['active_menu'] = 'gallery'  # 修改为 gallery
        context['active_submenu'] = 'sku'  # 添加 active_submenu
        
        # 获取有 SKU 关联的类目
        context['categories'] = Category.objects.filter(
            spus__skus__isnull=False
        ).annotate(
            sku_count=Count('spus__skus')  # 统计每个类目下的 SKU 数量
        ).order_by('category_name_en').distinct()
        
        # 安全地获取 category_id
        category_id = self.request.GET.get('category', '')
        context['category_id'] = int(category_id) if category_id.isdigit() else 0
        
        # 获取所有可选的颜色、材质和电镀工艺，并按值排序
        context['colors'] = SKU.objects.exclude(
            Q(color__isnull=True) | Q(color='')
        ).values('color').annotate(
            count=Count('id')
        ).order_by('color').values_list('color', flat=True)
        
        context['materials'] = SKU.objects.exclude(
            Q(material__isnull=True) | Q(material='')
        ).values('material').annotate(
            count=Count('id')
        ).order_by('material').values_list('material', flat=True)
        
        context['platings'] = SKU.objects.exclude(
            Q(plating_process__isnull=True) | Q(plating_process='')
        ).values('plating_process').annotate(
            count=Count('id')
        ).order_by('plating_process').values_list('plating_process', flat=True)
        
        # 当前选中的筛选值
        context['selected_color'] = self.request.GET.get('color', '')
        context['selected_material'] = self.request.GET.get('material', '')
        context['selected_plating'] = self.request.GET.get('plating', '')
        
        # 获取所有产品类型选项，包含显示名称
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
        
        # 当前选中的产品类型
        context['selected_product_type'] = self.request.GET.get('product_type', '')
        
        return context

class SKUCreateView(LoginRequiredMixin, CreateView):
    model = SKU
    template_name = 'gallery/sku_form2.html'
    form_class = SKUForm
    success_url = reverse_lazy('gallery:sku_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新增SKU'
        context['active_menu'] = 'gallery'
        context['active_submenu'] = 'sku'
        
        # 获取所有SPU并添加必要的字段
        spus = SPU.objects.filter(status=True).order_by('-created_at')
        for spu in spus:
            # 确保所有字段都存在
            spu.poc_id = spu.poc.id if spu.poc else ''
        context['spus'] = spus
        
        # 获取所有可用的类目
        context['categories'] = Category.objects.filter(status=True).order_by('level', 'rank_id')
        
        # 获取所有专员
        context['pocs'] = User.objects.filter(is_active=True).order_by('username')
        
        # 获取最新的SKU ID并生成新的SKU编码
        try:
            latest_sku = SKU.objects.latest('id')
            next_id = latest_sku.id + 1
        except SKU.DoesNotExist:
            next_id = 1
        
        context['generated_sku_code'] = f'SKU{next_id:06d}'  # 生成6位数的编码
        return context

    def form_valid(self, form):
        try:
            # 检查是否是新建SPU
            if self.request.POST.get('spu_selection') == 'create':
                # 获取最新的SPU ID并生成新的SPU编码
                try:
                    latest_spu = SPU.objects.latest('id')
                    next_spu_id = latest_spu.id + 1
                except SPU.DoesNotExist:
                    next_spu_id = 1
                
                spu_code = f'SPU{next_spu_id:06d}'
                
                # 创建新的SPU
                spu = SPU.objects.create(
                    spu_code=spu_code,
                    spu_name=form.cleaned_data.get('sku_name'),  # 使用SKU名称作为SPU名称
                    product_type=self.request.POST.get('product_type'),
                    sales_channel=self.request.POST.get('sales_channel'),
                    brand=self.request.POST.get('brand'),
                    poc_id=self.request.POST.get('poc')
                )
                # 设置SKU的SPU
                form.instance.spu = spu
            else:
                # 如果是引用现有SPU，确保已选择了SPU
                if not form.cleaned_data.get('spu'):
                    form.add_error('spu', '请选择一个SPU')
                    return self.form_invalid(form)
            
            messages.success(self.request, 'SKU创建成功！')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'SKU创建失败：{str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)

class SKUUpdateView(LoginRequiredMixin, UpdateView):
    model = SKU
    template_name = 'gallery/sku_form.html'
    form_class = SKUForm
    success_url = reverse_lazy('gallery:sku_list')
    login_url = '/muggle/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '编辑SKU'
        context['active_menu'] = 'gallery'
        context['active_submenu'] = 'sku'
        context['spus'] = SPU.objects.filter(status=True).order_by('-created_at')
        return context

    def form_valid(self, form):
        try:
            # 处理空值，设置默认值为0
            if not form.cleaned_data.get('length'):
                form.instance.length = 0
            if not form.cleaned_data.get('width'):
                form.instance.width = 0
            if not form.cleaned_data.get('height'):
                form.instance.height = 0
            if not form.cleaned_data.get('weight'):
                form.instance.weight = 0
            
            # 处理其他尺寸字段
            other_dimensions = form.cleaned_data.get('other_dimensions')
            if other_dimensions:
                form.instance.other_dimensions = other_dimensions[:25]  # 确保不超过25个字符
                
            response = super().form_valid(form)
            messages.success(self.request, 'SKU更新成功！')
            return response
        except Exception as e:
            messages.error(self.request, f'SKU更新失败：{str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            field_name = form.fields[field].label or field
            for error in errors:
                messages.error(self.request, f'{field_name}: {error}')
        return super().form_invalid(form)

class SKUDeleteView(LoginRequiredMixin, DeleteView):
    model = SKU
    success_url = reverse_lazy('gallery:sku_list')
    login_url = '/muggle/login/'
    template_name = 'gallery/sku_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '删除SKU'
        context['active_menu'] = 'gallery'
        context['active_submenu'] = 'sku'
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

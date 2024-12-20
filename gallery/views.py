from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category
from django.contrib import messages

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

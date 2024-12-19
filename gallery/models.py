from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid
import os
from django.core.validators import MinValueValidator

def category_image_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        new_filename = f"category_{instance.pk}_{instance.category_name_en}.{ext}"
    else:
        new_filename = f"category_{uuid.uuid4().hex[:8]}_{instance.category_name_en}.{ext}"
    return os.path.join('categories', new_filename)

class Category(models.Model):
    STATUS_CHOICES = (
        (1, '启用'),
        (0, '禁用'),
    )
    
    LEVEL_CHOICES = (
        (1, '一级分类'),
        (2, '二级分类'),
        (3, '三级分类'),
    )

    id = models.AutoField(primary_key=True, verbose_name='分类ID')
    category_name_en = models.CharField(max_length=100, verbose_name='英文名称')
    category_name_zh = models.CharField(max_length=100, verbose_name='中文名称')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    image = models.ImageField(
        upload_to=category_image_path, 
        blank=True, 
        null=True, 
        verbose_name='分类图片'
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='父分类'
    )
    rank_id = models.IntegerField(default=0, verbose_name='排序ID')
    original_data = models.TextField('原始数据', blank=True, null=True)
    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=1,
        verbose_name='分类层级'
    )
    is_last_level = models.BooleanField(
        default=False, 
        verbose_name='是否最后一级'
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1,
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'gallery_category'
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['rank_id', 'id']

    def __str__(self):
        return f"{self.category_name_zh} ({self.category_name_en})"

    def clean(self):
        if self.parent:
            if self.level <= self.parent.level:
                raise ValidationError('子类目的层级必须大于父类目的层级')
        elif self.level != 1:
            raise ValidationError('没有父类目时，必须是一级分类')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        if self.image and not self.image.name.startswith(f'categories/category_{self.pk}_'):
            old_path = self.image.path
            filename = os.path.basename(self.image.name)
            ext = filename.split('.')[-1]
            
            new_filename = f"category_{self.pk}_{self.category_name_en}.{ext}"
            new_path = os.path.join('categories', new_filename)
            
            self.image.name = new_path
            super().save(update_fields=['image'])
            
            if os.path.exists(old_path):
                new_full_path = os.path.join(settings.MEDIA_ROOT, new_path)
                os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
                os.rename(old_path, new_full_path)

    @property
    def full_name(self):
        if self.parent:
            return f"{self.parent.full_name} > {self.category_name_zh}"
        return self.category_name_zh

class SPU(models.Model):
    CHANNEL_CHOICES = (
        (1, '线上'),
        (2, '线下'),
        (3, '全渠道'),
    )

    PRODUCT_TYPE_CHOICES = (
        ('math_design', '设计款'),     # 设计款产品
        ('ready_made', '现货款'),      # 现货款产品
        ('raw_material', '材料'),      # 原材料
        ('packing_material', '包材'),  # 包装材料
    )

    id = models.AutoField(primary_key=True, verbose_name='SPU ID')
    spu_code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='SPU编码'
    )
    spu_name = models.CharField(
        max_length=200, 
        verbose_name='SPU名称'
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='ready_made',    # 默认为现货款
        verbose_name='产品类型'
    )
    spu_remark = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='备注'
    )
    sales_channel = models.IntegerField(
        choices=CHANNEL_CHOICES,
        default=3,
        verbose_name='销售渠道'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='spus',
        verbose_name='所属类目'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.BooleanField(default=True, verbose_name='状态')

    class Meta:
        db_table = 'gallery_spu'
        verbose_name = 'SPU'
        verbose_name_plural = 'SPU列表'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['spu_code']),
            models.Index(fields=['category']),
            models.Index(fields=['sales_channel']),
        ]

    def __str__(self):
        return f"{self.spu_code} - {self.spu_name}"

    def clean(self):
        if self.spu_code and len(self.spu_code) < 4:
            raise ValidationError({
                'spu_code': 'SPU编码长度不能小于4个字符'
            })
        
        if self.category and not self.category.is_last_level:
            raise ValidationError({
                'category': '只能选择最后一级类目'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def channel_display(self):
        return self.get_sales_channel_display()

    @property
    def category_full_name(self):
        return self.category.full_name if self.category else ''

class SKU(models.Model):
    PLATING_PROCESS_CHOICES = (
        ('none', '无电镀'),
        ('gold', '镀金'),
        ('silver', '镀银'),
        ('nickel', '镀镍'),
        ('chrome', '镀铬'),
        ('copper', '镀铜'),
        ('other', '其他'),
    )

    id = models.AutoField(primary_key=True, verbose_name='SKU ID')
    sku_code = models.CharField(max_length=32, unique=True, verbose_name='SKU编码')
    sku_name = models.CharField(max_length=128, verbose_name='SKU名称')
    provider_code = models.CharField(
        max_length=32, 
        default='unknown',
        verbose_name='供应商编码'
    )
    plating_process = models.CharField(max_length=32, choices=PLATING_PROCESS_CHOICES, verbose_name='电镀工艺')
    color = models.CharField(max_length=32, verbose_name='颜色')
    material = models.CharField(max_length=100, default='无', verbose_name='材质')
    length = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='长度(mm)'
    )
    width = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='宽度(mm)'
    )
    height = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='高度(mm)'
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='重量(g)')
    status = models.BooleanField(default=True, verbose_name='状态')
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, related_name='skus', verbose_name='所属SPU')
    img_url = models.CharField(max_length=255, blank=True, null=True, verbose_name='图片URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'gallery_sku'
        verbose_name = 'SKU'
        verbose_name_plural = 'SKU列表'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sku_code']),
            models.Index(fields=['spu']),
            models.Index(fields=['created_at']),
        ]
        permissions = [
            ("sync_sku", "Can synchronize SKU data"),
        ]

    def __str__(self):
        return f"{self.sku_code} - {self.sku_name}"

    def clean(self):
        if self.sku_code and len(self.sku_code) < 4:
            raise ValidationError({
                'sku_code': 'SKU编码长度不能小于4个字符'
            })

    def save(self, *args, **kwargs):
        if not self.provider_code:
            self.provider_code = 'unknown'
        if not self.plating_process:
            self.plating_process = 'none'
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.spu.spu_name} - {self.sku_name}"

    @property
    def dimensions(self):
        return f"{self.length}*{self.width}*{self.height}mm"

    @property
    def volume(self):
        return float(self.length) * float(self.width) * float(self.height)

    @property
    def volume_m3(self):
        return self.volume / 1000000000

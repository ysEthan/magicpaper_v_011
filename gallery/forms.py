from django import forms
from .models import SKU

class SKUForm(forms.ModelForm):
    class Meta:
        model = SKU
        fields = ['sku_code', 'sku_name', 'suppliers_list', 'plating_process', 
                 'color', 'material', 'length', 'width', 'height', 'weight', 
                 'other_dimensions', 'status', 'spu', 'img_url']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 将数值字段设置为非必填
        self.fields['weight'].required = False
        self.fields['length'].required = False
        self.fields['width'].required = False
        self.fields['height'].required = False
        self.fields['other_dimensions'].required = False
        
        # 设置其他尺寸字段的属性
        self.fields['other_dimensions'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '其他尺寸',
            'maxlength': '25'
        }) 
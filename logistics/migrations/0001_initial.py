# Generated by Django 4.2.16 on 2024-12-23 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trade', '0002_alter_order_buyer_remark_alter_order_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name_zh', models.CharField(max_length=25, verbose_name='中文名称')),
                ('name_en', models.CharField(max_length=25, verbose_name='英文名称')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='物流商代码')),
                ('url', models.URLField(blank=True, verbose_name='官网地址')),
                ('contact', models.CharField(blank=True, max_length=20, verbose_name='联系电话')),
                ('key', models.IntegerField(blank=True, null=True, verbose_name='查询代码')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '物流商',
                'verbose_name_plural': '物流商',
                'db_table': 'logistics_carrier',
                'ordering': ['name_zh'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=25, verbose_name='服务名称')),
                ('service_code', models.CharField(max_length=10, verbose_name='服务代码')),
                ('service_type', models.IntegerField(verbose_name='服务类型')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.carrier', verbose_name='物流商')),
            ],
            options={
                'verbose_name': '物流服务',
                'verbose_name_plural': '物流服务',
                'db_table': 'logistics_service',
                'ordering': ['carrier', 'service_name'],
                'unique_together': {('carrier', 'service_code')},
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_no', models.CharField(blank=True, max_length=30, null=True, verbose_name='跟踪号')),
                ('pkg_status_code', models.CharField(default='0', max_length=4, verbose_name='包裹状态码')),
                ('items', models.JSONField(help_text='包含SKU、品名、包裹尺寸、重量等信息', verbose_name='商品列表')),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='运费')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.order', verbose_name='订单')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logistics.service', verbose_name='物流服务')),
            ],
            options={
                'verbose_name': '包裹',
                'verbose_name_plural': '包裹',
                'db_table': 'logistics_package',
                'ordering': ['-created_at'],
            },
        ),
    ]
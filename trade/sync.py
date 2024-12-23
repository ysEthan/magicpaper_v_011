import time
import hashlib
import json
import math
import requests
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Order, Shop, Cart
from gallery.models import SKU  # 避免循环导入

# 获取logger实例
logger = logging.getLogger(__name__)

def generate_sign(body):
    """生成API签名"""
    appName = "mathmagic"
    appKey = "82be0592545283da00744b489f758f99"
    sid = "mathmagic"

    headers = {
        'Content-Type': 'application/json'
    }

    timestamp = str(int(time.time()))
    sign_str = "{appKey}appName{appName}body{body}sid{sid}timestamp{timestamp}{appKey}".format(
        appKey=appKey, appName=appName, body=body, sid=sid, timestamp=timestamp
    )
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    
    params = {
        "appName": appName,
        "sid": sid,
        "sign": sign,
        "timestamp": timestamp,
    }
    return params, headers

def get_trade_detail(trade_id):
    """获取订单明细数据"""
    body = {
        "tradeIds": [str(trade_id)]
    }
    body_str = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    params, headers = generate_sign(body_str)
    
    url = "https://openapi.qizhishangke.com/api/openservices/trade/v1/getSalesTradeOrderList"
    response = requests.post(url, params=params, headers=headers, data=body_str)

    # 打印返回的数据结构
    print("API返回数据:", response.json()['data'] )


    if response.status_code != 200:
        raise Exception(f"API请求失败: {response.text}")
        
    response_data = response.json()
    if response_data['code'] != 200:
        raise Exception(f"API返回错误: {response_data['message']}")
    

    
    return response_data['data']

def sync_trade_detail(order, trade_id):
    """同步订单商品明细"""
    try:
        # 获取订单明细数据
        details = get_trade_detail(trade_id)
        
        # 删除原有的购物车记录
        Cart.objects.filter(order=order).delete()
        
        # 同步商品明细
        for item in details:
            try:
                # 使用正确的字段名获取SKU编码
                sku_code = item.get('skuNo')
                if not sku_code:
                    logger.error(f"找不到SKU编码字段, 订单号: {order.order_no}, 数据: {item}")
                    continue
                    
                sku = SKU.objects.get(sku_code=sku_code)
                
                # 创建购物车记录
                Cart.objects.create(
                    order=order,
                    sku=sku,
                    qty=int(item.get('num', 1)),
                    price=float(item.get('price', 0)),
                    cost=float(item.get('cost', 0)),
                    discount=float(item.get('discount', 0)),
                    actual_price=float(item.get('actualPrice', item.get('price', 0))),
                    is_out_of_stock=False
                )
            except SKU.DoesNotExist:
                logger.error(f"找不到SKU: {sku_code}, 订单号: {order.order_no}")
                continue
            except Exception as e:
                logger.error(f"处理订单商品明细时出错: {str(e)}, 订单号: {order.order_no}")
                continue
                
    except Exception as e:
        logger.error(f"获取订单明细数据失败: {str(e)}, 订单号: {order.order_no}")

def sync_trade_data(start_date, end_date, page=1):
    """同步订单数据"""
    body = {
        "createTimeBegin": start_date,
        "createTimeEnd": end_date,
        "tradeStatusCode": 0,
        "pageNo": page,
        "pageSize": 100
    }
    body_str = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    params, headers = generate_sign(body_str)
    
    url = "https://openapi.qizhishangke.com/api/openservices/trade/v1/getSalesTradeList"
    response = requests.post(url, params=params, headers=headers, data=body_str)
    
    if response.status_code != 200:
        raise Exception(f"API请求失败: {response.text}")
        
    response_data = response.json()
    if response_data['code'] != 200:
        raise Exception(f"API返回错误: {response_data['message']}")
        
    data = response_data['data']
    
    for item in data['data']:
        # 处理时间字段
        created_time = datetime.strptime(item['tradeTime'], "%Y-%m-%dT%H:%M:%S")
        try:
            shiped_time = datetime.strptime(item['deliveryTime'], "%Y-%m-%dT%H:%M:%S")
            shiped_date = shiped_time.date()
        except:
            shiped_time = None
            shiped_date = None
            
        try:
            operate_time = datetime.strptime(item['outBoundTime'], "%Y-%m-%dT%H:%M:%S")
        except:
            operate_time = None

        # 获取或创建Shop
        shop, _ = Shop.objects.get_or_create(
            code=item['shopNo'],
            defaults={
                'name': item['shopText'],
                'is_active': True
            }
        )

        # 状态映射
        status_mapping = {
            '待发货': Order.OrderStatus.PENDING,
            '已发货': Order.OrderStatus.SHIPPED,
            '已完成': Order.OrderStatus.COMPLETED,
            '已取消': Order.OrderStatus.CANCELLED,
            # 添加其他状态映射...
        }

        # 更新或创建Order
        order_data = {
            'platform_order_no': item['srcTids'],
            'order_no': item['tradeNo'],
            'recipient_country': item['country'],
            'recipient_state': item['receiverProvince'],
            'created_at': created_time,
            'shop': shop,
            'status': status_mapping.get(item['tradeStatusDesc'], Order.OrderStatus.PENDING),
            'paid_amount': 0.00,
            'freight': 0.00,
            'recipient_name': item['receiverName'],
            'recipient_phone': item['receiverMobile'],
            'recipient_email': '',
            'recipient_city': item['receiverCity'],
            'recipient_address': item['receiverAddress'],
            'system_remark': item['erpRemark'],
            'cs_remark': item['csRemark'],
            'buyer_remark': item['buyerMessage']
        }

        try:
            # 创建或更新订单
            order, created = Order.objects.update_or_create(
                id=item['tradeId'],
                defaults=order_data
            )
            print('处理订单', item['srcTids'], '成功============================================================')
            # 同步订单商品明细
            sync_trade_detail(order, item['tradeId'])
            
        except Exception as e:
            logger.error(f"处理订单 {item['srcTids']} 时出错: {str(e)}")
            continue
    
    # 处理分页
    if page < math.ceil(data['total'] / data['pageSize']):
        sync_trade_data(start_date, end_date, page + 1)

def sync_all_trade():
    """同步所有订单数据的入口函数"""
    try:
        # 默认同步最近7天的数据
        end_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (timezone.now() - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
        sync_trade_data(start_date, end_date)
        return True, "订单数据同步成功"
    except Exception as e:
        return False, f"订单数据同步失败: {str(e)}" 
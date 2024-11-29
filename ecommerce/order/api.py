from ninja import NinjaAPI

from ecommerce.order.models import Order, ShippingAddress
from ecommerce.order.schema import OrderSchema
from typing import List

api = NinjaAPI()


@api.get("/get_pending_orders", response=List[OrderSchema])
def google_sheets_pull(request):
    orders = Order.objects.all()
    order_data = []
    for order in orders:
        order_items = []
        for item in order.items.all():
            if item.item.type == 'Package':
                volume_name = item.item.product.name + ' - ' + str(item.item.package_name)
            else:
                volume_name = item.item.product.name + ' - ' + str(item.item.volume_number)

            order_items.append({
                'item': volume_name,
                'language': item.language,
                'quantity': item.quantity
            })
        shipping_address = ShippingAddress.objects.filter(user=order.user).order_by('-created_at').first()

        order_data.append({
            'id': order.id,
            'user': order.user,
            'total_price': order.total_price.amount,
            'total_quantity': order.total_quantity,
            'status': order.status,
            'uuid': order.uuid,
            'items': order_items,
            'shipping_address': {
                "name": shipping_address.name,
                "province": shipping_address.province,
                "address": shipping_address.address,
                "phone": shipping_address.phone,
                "phone2": shipping_address.phone2,
                "email": shipping_address.email,
                "instagram_username": shipping_address.instagram_username
            }
        })
    return order_data

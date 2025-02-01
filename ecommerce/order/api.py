import hashlib
import hmac
import json
from typing import List

from django.conf import settings
from ninja import NinjaAPI

from ecommerce.abstract.models.choices import ProvinceChoices
from ecommerce.home.models import Global
from ecommerce.order.models import Order, ShippingAddress
from ecommerce.order.schema import OrderSchema

api = NinjaAPI()

def check_hmac_request(request):
    signature = request.headers.get("X-HMAC-Signature")
    if not signature:
        raise Exception(400, "HMAC signature missing from headers.")

    # Use Django's SECRET_KEY as the key (encoded to bytes)
    secret_key = settings.SECRET_KEY.encode("utf-8")
    # Compute the HMAC signature on the raw request body
    print(request.body)
    print(secret_key)
    computed_signature = hmac.new(secret_key, request.body, hashlib.sha256).hexdigest()
    print(computed_signature)

    # Compare the computed signature to the one that came in the header
    if not hmac.compare_digest(signature, computed_signature):
        raise Exception(403, "Invalid HMAC signature.")

    return True

@api.get("/get_pending_orders", response=List[OrderSchema])
def google_sheets_pull(request):
    check_hmac_request(request)
    orders = Order.objects.filter(status=Order.Status_CHOICES.CONFIRMED)
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
        delivery_price = Global.get_instance().delivery_price
        if shipping_address.province != ProvinceChoices.BAGHDAD:
            delivery_price = Global.get_instance().delivery_price_outside_baghdad
        order_data.append({
            'id': order.id,
            'user': order.user,
            'total_price': order.total_price.amount,
            'delivery_price': delivery_price.amount,
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
    # orders.update(status=Order.Status_CHOICES.PLACED_ON_SHEET)
    return order_data


@api.post("/posted_placed_orders", )
def post_placed_orders(request):
    check_hmac_request(request)

    # If signature verification passed, decode the request body
    data = request.body.decode('utf-8')
    json_data = json.loads(data)

    # Extract the ids field from the JSON data
    ids = json_data.get('ids', [])

    # Update the status of the orders with the provided ids
    Order.objects.filter(id__in=ids).update(status=Order.Status_CHOICES.ON_WORK)

    return {"message": "Orders updated successfully."}
# def google_sheets_pull(request):
# orders = Order.objects.filter(status=Order.Status_CHOICES.CONFIRMED)
# order_data = []
# for order in orders:
#     order_items = []
#     for item in order.items.all():
#         if item.item.type == 'Package':
#             volume_name = item.item.product.name + ' - ' + str(item.item.package_name)
#         else:
#             volume_name = item.item.product.name + ' - ' + str(item.item.volume_number)
#
#         order_items.append({
#             'item': volume_name,
#             'language': item.language,
#             'quantity': item.quantity
#         })
#     shipping_address = ShippingAddress.objects.filter(user=order.user).order_by('-created_at').first()
#     delivery_price = Global.get_instance().delivery_price
#     if shipping_address.province != ProvinceChoices.BAGHDAD:
#         delivery_price = Global.get_instance().delivery_price_outside_baghdad
#     order_data.append({
#         'id': order.id,
#         'user': order.user,
#         'total_price': order.total_price.amount,
#         'delivery_price': delivery_price.amount,
#         'total_quantity': order.total_quantity,
#         'status': order.status,
#         'uuid': order.uuid,
#         'items': order_items,
#         'shipping_address': {
#             "name": shipping_address.name,
#             "province": shipping_address.province,
#             "address": shipping_address.address,
#             "phone": shipping_address.phone,
#             "phone2": shipping_address.phone2,
#             "email": shipping_address.email,
#             "instagram_username": shipping_address.instagram_username
#         }
#     })
# # orders.update(status=Order.Status_CHOICES.PLACED_ON_SHEET)
# return order_data

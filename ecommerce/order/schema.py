from typing import List

from ninja import Schema


class OrderItemSchema(Schema):
    item: str
    language: str
    quantity: int


class ShippingAddressSchema(Schema):
    name: str
    address: str
    province: str
    phone: str
    phone2: str
    instagram_username: str

class OrderSchema(Schema):
    items: List[OrderItemSchema] = []
    shipping_address: ShippingAddressSchema
    id: int
    total_price: float
    delivery_price: float
    total_quantity: int
    status: str
    uuid: str
# class OrderSchema(ModelSchema):
#     items: List[OrderItemSchema] = []
#     class Meta:
#         model = Order
#
#         fields = ['id', 'user', 'total_price', 'total_quantity', 'status', 'uuid']

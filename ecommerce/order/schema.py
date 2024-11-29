from ninja import ModelSchema
from typing import List

from ecommerce.order.models import Order, OrderItem


class OrderItemSchema(ModelSchema):
    class Meta:
        model = OrderItem

        fields = "__all__"


class OrderSchema(ModelSchema):
    items: List[OrderItemSchema] = []

    class Meta:
        model = Order

        fields = ['id', 'user', 'total_price', 'total_quantity', 'status', 'uuid']

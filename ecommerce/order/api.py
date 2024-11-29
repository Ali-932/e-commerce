from ninja import NinjaAPI

from ecommerce.order.models import Order
from ecommerce.order.schema import OrderSchema

api = NinjaAPI()


@api.get("/get_pending_orders", response=OrderSchema)
def google_sheets_pull(request):
    orders = Order.objects.all()
    print(orders)
    return orders

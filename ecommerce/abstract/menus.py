from django.urls import reverse_lazy, reverse
from simple_menu import Menu, MenuItem

from ecommerce.abstract.utlites.menu_nums import menu_nums, CategoryChoices

manga_children = [
    MenuItem(
        "المانجا",
        url=reverse('product:list-products'),
        icon='people-line',
        column=1,
    ),
    MenuItem(
        "المانهوا",
        url='',
        icon='cart-arrow-up',
        column=1,
    ),
    MenuItem(
        "الكوميك",
        url='',
        icon='file-invoice',
        column=1,
    ),
MenuItem(
        "البكجات",
        url='',
        icon='file-invoice',
        column=1,
    ),
# MenuItem(
#     'ايسيكاي',
#     url='',
#     icon='Isekai',
#     column=2,
# ),
# MenuItem(
#     'الرومانسية',
#     url='',
#     icon='Romance',
#     column=2,
# ),
# MenuItem(
#     'الكوميديا',
#     url='',
#     icon='Comedy',
#     column=2,
# ),
# MenuItem(
#     'شريحة من الحياة',
#     url='',
#     icon='Slice of Life',
#     column=2,
# ),
# MenuItem(
#     'الميكا',
#     url='',
#     icon='Mecha',
#     column=2,
# ),
# MenuItem(
#     'الرعب',
#     url='',
#     icon='Horror',
#     column=2,
# ),
# MenuItem(
#     'الرياضة',
#     url='',
#     icon='Sports',
#     column=2,
# ),
# MenuItem(
#     'شوتا',
#     url='',
#     icon='Shota',
#     column=2,
# )

]

Menu.add_item('onesight',
              MenuItem(
                  'الرئيسية',
                  icon='home',
                  url=reverse('home:index'),
                  weight=20,
                  num=menu_nums.get('home', 0)
              ))

Menu.add_item('onesight',
              MenuItem(
                  'المنتجات',
                  # icon='receipt',
                  url=reverse('product:list-products'),
                  weight=20,
                  children=manga_children,
                  columns=[1, 2],
                  num=menu_nums.get('products', 1)

              ))

Menu.add_item('onesight',
              MenuItem(
                  'عروض خاصة',
                  icon='warehouse-full',
                  url='',
                  weight=20,
                  # children=inventory_children,
                  columns=[1, 2],
                  num=menu_nums.get('best_sellers', 2)
              ))
Menu.add_item('onesight',
              MenuItem(
                  'حزمة مجلدات',
                  icon='diagram-project',
                  url='',
                  weight=20,
                  # children=project_children,
                  columns=[1, ],
                  num=menu_nums.get('new_arrival', 3)
              ))
Menu.add_item('onesight',
              MenuItem(
                  'نبذة عنا',
                  icon='people-simple',
                  url=reverse('home:quality_rep'),
                  weight=20,
                  columns=[1, ],
                  num= menu_nums.get('about', 4)
              ))

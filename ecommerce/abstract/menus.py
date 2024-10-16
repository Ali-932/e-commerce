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
                  url=reverse('product:list-special-offer-products'),
                  weight=20,
                  # children=inventory_children,
                  columns=[1, 2],
                  num=menu_nums.get('special-offers', 2)
              ))
Menu.add_item('onesight',
              MenuItem(
                  'حزمة مجلدات',
                  icon='diagram-project',
                  url=reverse('product:list-package-products'),
                  weight=20,
                  # children=project_children,
                  columns=[1,2],
                  num=menu_nums.get('packages', 3)
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

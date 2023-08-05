from django.urls import reverse_lazy, reverse
from simple_menu import Menu, MenuItem

from ecommerce.abstract.utlites.menu_nums import menu_nums, CategoryChoices

manga_children = [
    MenuItem(
        CategoryChoices.SHONEN,
        url='',
        icon='people-line',
        column=1,
    ),
    MenuItem(
        CategoryChoices.KODOMO,
        url='',
        icon='cart-arrow-up',
        column=1,
    ),
    MenuItem(
        CategoryChoices.SEINEN,
        url='',
        icon='file-invoice',
        column=1,
    ),
    MenuItem(
        CategoryChoices.SHOUJO,
        url='',
        icon='arrow-left',
        column=1,
    ),
    MenuItem(
        CategoryChoices.JOSEI,
        url='',
        icon='file-import',
        column=1,
    ),
    MenuItem(
        CategoryChoices.SEIJIN,
        url='',
        icon='file-alt',
        column=1,
    ),
    MenuItem(
        CategoryChoices.REDISU,
        url='',
        icon='forklift',
        column=1
    ),
    MenuItem(
        CategoryChoices.GEKIGA,
        url='',
        icon='list-alt',
        column=1
    ),
MenuItem(
    'ايسيكاي',
    url='',
    icon='Isekai',
    column=2,
),
MenuItem(
    'الرومانسية',
    url='',
    icon='Romance',
    column=2,
),
MenuItem(
    'الكوميديا',
    url='',
    icon='Comedy',
    column=2,
),
MenuItem(
    'شريحة من الحياة',
    url='',
    icon='Slice of Life',
    column=2,
),
MenuItem(
    'الميكا',
    url='',
    icon='Mecha',
    column=2,
),
MenuItem(
    'الرعب',
    url='',
    icon='Horror',
    column=2,
),
MenuItem(
    'الرياضة',
    url='',
    icon='Sports',
    column=2,
),
MenuItem(
    'شوتا',
    url='',
    icon='Shota',
    column=2,
)

]

inventory_children = [
    MenuItem(
        'المستودعات',
        url='',
        icon='warehouse-full',
        column=1,
    ),
    MenuItem(
        'الأصول المخزنية والخدمات',
        url='',
        icon='box-circle-check',
        column=1,
    ),
    MenuItem(
        'مستندات الإخراج المخزني',
        url='',
        icon='file-export',
        column=1,
    ),
    MenuItem(
        'مستندات الاستلام المخزني',
        url='',
        icon='file-import',
        column=1,
    ),
    MenuItem(
        'محضر إتلاف المخزون',
        url='',
        icon='trash-xmark',
        column=1,
    ),
    MenuItem(
        'نقل المخزون',
        url='',
        icon='arrow-right-arrow-left',
        column=1,
    ),
    MenuItem(
        'زيادة الجرد المخزني',
        url='',
        icon='up',
        column=1,
    ),
    MenuItem(
        'نقص الجرد المخزني',
        url='',
        icon='down',
        column=1,
    ),
    MenuItem(
        '-',
        url='',
        column=2,
    ),
    MenuItem(
        'الأصول الثابتة / المحاسبية',
        url='',
        icon='chair-office',
        column=2
    ),
    MenuItem(
        'الأصول غير الملموسة',
        url='',
        icon='compact-disc',
        column=2
    ),
    MenuItem(
        'طلبات الأصل الثابت',
        url='',
        icon='cart-circle-arrow-down',
        column=2
    ),
    MenuItem(
        'مشتريات الأصل الثابت',
        url='',
        icon='file-invoice',
        column=2
    ),
    MenuItem(
        'محضر شطب الأصل الثابت',
        url='',
        icon='trash-xmark',
        column=2
    ),
    MenuItem(
        'محضر إطفاء الأصل غير الملموس',
        url='',
        icon='trash-xmark',
        column=2
    ),
]

project_children = [
    MenuItem(
        'إدارة المشاريع',
        url='',
        icon='chart-gantt',
        column=1
    ),
    MenuItem(
        'أوامر العمل',
        url='',
        icon='bars-progress',
        column=1
    ),
    MenuItem(
        'أوامر الصيانة',
        url='',
        icon='chart-line',
        column=1
    ),
]

hr_children = [
    MenuItem(
        'هيكل المؤسسة',
        url='',
        icon='sitemap',
        column=1
    ),
    MenuItem(
        'الفروع',
        url='',
        icon='code-branch',
        column=1
    ),
    MenuItem(
        'الأقسام',
        url='',
        icon='code-fork',
        column=1
    ),
    MenuItem(
        'الشُعب',
        url='',
        icon='users',
        column=1
    ),
    MenuItem(
        'الموظفون',
        url='',
        icon='user-alt',
        column=1
    ),
    MenuItem(
        'مكونات الراتب',
        url='',
        icon='list-alt',
        column=1
    ),
    MenuItem(
        'قوالب قسيمة الرواتب',
        url='',
        icon='list-alt',
        column=1
    ),
    MenuItem(
        'قسيمة الرواتب الدورية',
        url='',
        icon='file-circle-exclamation',
        column=1
    ),
    MenuItem(
        'سند ائتمان للموظف',
        url='',
        icon='file-alt',
        column=1
    ),
]

accounting_children = [
    MenuItem(
        'قائمة الحسابات (ميزان المراجعة التفصيلي)',
        url='',
        icon='bank',
        column=1
    ),
    # MenuItem(
    #     'ميزان المراجعة العام',
    #     url=reverse_lazy('accounting:trial-balance-summary'),
    #     icon='scale-balanced',
    #     column=1
    # ),
    MenuItem(
        'سند قيد',
        url='',
        icon='money-bill-transfer',
        column=1
    ),
    MenuItem(
        'جميع السندات',
        url='',
        icon='money-bill-1-wave',
        column=1
    ),
    # MenuItem(
    #     'تدقيق السندات غير المتوازنة',
    #     url='',
    #     icon='money-bill-wave-alt',
    #     column=1
    # ),
    # MenuItem(
    #     'جميع القيود',
    #     url='',
    #     icon='money-bill-alt',
    #     column=1
    # ),
    MenuItem(
        'مراكز الكلف',
        url='',
        icon='arrows-to-dot',
        column=1
    ),
    MenuItem(
        'مراكز الربح',
        url='',
        icon='arrows-to-circle',
        column=1
    ),
    MenuItem(
        'مراكز العمل',
        url='',
        icon='arrows-to-dotted-line',
        column=1
    ),
]

reports_children = [
    MenuItem(
        'قائمة المركز المالي',
        url='',
        icon='chart-column',
        column=1,
    ),
    MenuItem(
        'قائمة الدخل',
        url='',
        icon='file-chart-column',
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
                  'الاكثر مبيعا',
                  icon='warehouse-full',
                  url='',
                  weight=20,
                  children=inventory_children,
                  columns=[1, 2],
                  num=menu_nums.get('best_sellers', 2)
              ))
Menu.add_item('onesight',
              MenuItem(
                  'المضاف حديثاً',
                  icon='diagram-project',
                  url='',
                  weight=20,
                  children=project_children,
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

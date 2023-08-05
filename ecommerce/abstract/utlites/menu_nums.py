from django.db import models

menu_nums = {
    'home': 0,
    'products': 1,
    'best_sellers': 2,
    'new_arrival': 3,
    'about': 4,
}


class CategoryChoices(models.TextChoices):
    SHONEN = 'شونن', 'Shonen'  # Manga for young teenage boys, roughly between 12-18.
    KODOMO = 'كودومو', 'Kodomo'  # Manga for little kids or young children, under about 8.
    SEINEN = 'سينين', 'Seinen'  # Manga for young adult males or younger men, roughly between 18-40.
    SHOUJO = 'شوجو', 'Shoujo'  # Manga for young teenage girls, roughly between 8-18.
    JOSEI = 'جوسي', 'Josei'  # Manga for adult females or younger women, roughly between 18-40.
    SEIJIN = 'سيجين', 'Seijin'  # Adult manga for males.
    REDISU = 'ريديسو', 'Redisu'  # Manga for young adult females.
    GEKIGA = 'جيكيجا', 'Gekiga'  # Manga focusing on serious topics geared toward mature audiences.

    ISEKAI = 'ايسيكاي', 'Isekai'
    ROMANCE = 'الرومانسية', 'Romance'
    COMEDY = 'الكوميديا', 'Comedy'
    SLICE_OF_LIFE = 'شريحة من الحياة', 'Slice of Life'
    MECHA = 'الميكا', 'Mecha'
    HORROR = 'الرعب', 'Horror'
    SPORTS = 'الرياضة', 'Sports'
    SHOTA = 'شوتا', 'Shota'


'''
ISEKAI = 'ايسيكاي', 'Isekai'
ROMANCE = 'الرومانسية', 'Romance'
COMEDY = 'الكوميديا', 'Comedy'
SLICE_OF_LIFE = 'شريحة من الحياة', 'Slice of Life'
MECHA = 'الميكا', 'Mecha'
HORROR = 'الرعب', 'Horror'
SPORTS = 'الرياضة', 'Sports'
SHOTA = 'شوتا', 'Shota'
'''

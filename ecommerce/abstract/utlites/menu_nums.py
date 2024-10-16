from django.db import models

menu_nums = {
    'home': 0,
    'products': 1,
    'special-offers': 2,
    'packages': 3,
    'about': 4,
}


class ThemeChoices(models.TextChoices):
    MAHOU_SHOUJO = 'ماهو شوجو', 'Mahou Shoujo'
    SAMURAI = 'الساموراي', 'Samurai'
    ISEKAI = 'ايسيكاي', 'Isekai'
    SUPER_POWER = 'القوى الخارقة', 'Super Power'
    CROSSDRESSING = 'التنكر', 'Crossdressing'
    EDUCATIONAL = 'تعليمي', 'Educational'
    MECHA = 'الميكا', 'Mecha'
    PARODY = 'السخرية', 'Parody'
    REINCARNATION = 'التناسخ', 'Reincarnation'
    STRATEGY_GAME = 'لعبة استراتيجية', 'Strategy Game'
    IYASHIKEI = 'اياشيكي', 'Iyashikei'
    PSYCHOLOGICAL = 'نفسي', 'Psychological'
    ORGANIZED_CRIME = 'الجريمة المنظمة', 'Organized Crime'
    RACING = 'سباق', 'Racing'
    TIME_TRAVEL = 'السفر عبر الزمن', 'Time Travel'
    SPACE = 'الفضاء', 'Space'
    WORKPLACE = 'مكان العمل', 'Workplace'
    DETECTIVE = 'المحقق', 'Detective'
    SHOWBIZ = 'صناعة الترفيه', 'Showbiz'
    VISUAL_ARTS = 'الفنون البصرية', 'Visual Arts'
    ANTHROPOMORPHIC = 'متجسد', 'Anthropomorphic'
    GAG_HUMOR = 'نكتة فكاهية', 'Gag Humor'
    VILLAINESS = 'الشريرة', 'Villainess'
    OTAKU_CULTURE = 'ثقافة أوتاكو', 'Otaku Culture'
    HAREM = 'حريم', 'Harem'
    MARTIAL_ARTS = 'الفنون القتالية', 'Martial Arts'
    ROMANTIC_SUBTEXT = 'النص الرومانسي الفرعي', 'Romantic Subtext'
    PETS = 'الحيوانات الأليفة', 'Pets'
    VIDEO_GAME = 'لعبة فيديو', 'Video Game'
    SURVIVAL = 'البقاء على قيد الحياة', 'Survival'
    CGDCT = 'CGDCT', 'CGDCT'
    SCHOOL = 'المدرسة', 'School'
    HISTORICAL = 'تاريخي', 'Historical'
    MEDICAL = 'طبي', 'Medical'
    VAMPIRE = 'مصاص الدماء', 'Vampire'
    DELINQUENTS = 'المارقون', 'Delinquents'
    MILITARY = 'العسكري', 'Military'
    MUSIC = 'الموسيقى', 'Music'
    ADULT_CAST = 'فريق الكبار', 'Adult Cast'
    CHILDCARE = 'رعاية الأطفال', 'Childcare'
    GORE = 'العنف الدموي', 'Gore'
    MYTHOLOGY = 'الأساطير', 'Mythology'
    COMBAT_SPORTS = 'رياضات القتال', 'Combat Sports'
    REVERSE_HAREM = 'حريم معكوس', 'Reverse Harem'
    PERFORMING_ARTS = 'الفنون الأدائية', 'Performing Arts'
    MEMOIR = 'مذكرات', 'Memoir'
    TEAM_SPORTS = 'رياضات الفريق', 'Team Sports'
    LOVE_POLYGON = 'مضلع الحب', 'Love Polygon'
    HIGH_STAKES_GAME = 'لعبة المخاطر العالية', 'High Stakes Game'

class DemographicChoices(models.TextChoices):
    KIDS = 'كودومو', 'Kids'
    SHOUJO = 'شوجو', 'Shoujo'
    SHOUNEN = 'شونين', 'Shounen'
    SEINEN = 'سينين', 'Seinen'
    JOSEI = 'جوسي', 'Josei'

class GenresChoices(models.TextChoices):
    AWARD_WINNING = 'فائز بجوائز', 'Award Winning'
    ACTION = 'الأكشن', 'Action'
    ROMANCE = 'الرومانسية', 'Romance'
    COMEDY = 'الكوميديا', 'Comedy'
    HORROR = 'الرعب', 'Horror'
    MYSTERY = 'الغموض', 'Mystery'
    SUPERNATURAL = 'الخارق', 'Supernatural'
    SLICE_OF_LIFE = 'شريحة من الحياة', 'Slice of Life'
    GOURMET = 'الذوق الرفيع', 'Gourmet'
    SCI_FI = 'الخيال العلمي', 'Sci-Fi'
    SPORTS = 'الرياضة', 'Sports'
    FANTASY = 'الخيال', 'Fantasy'
    ADVENTURE = 'المغامرة', 'Adventure'
    SUSPENSE = 'التشويق والإثارة', 'Suspense'
    DRAMA = 'الدراما', 'Drama'

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

from django.core.management.base import BaseCommand
from ecommerce.product.models import *
from django.db.transaction import atomic

class ManhwaData:
    solo_leveling_info = {
        "name": "Solo Leveling",
        "genres": ["الأكشن", "المغامرة", "الخيال", "الفنون القتالية", "شونين"],
        "themes": ["Monsters", "الخارق"],
        "demographics": ["شونين"],
        "synopsis": "في عالم حيث يجب على الصيادين، البشر الذين يمتلكون قدرات سحرية، مواجهة الوحوش القاتلة لحماية البشرية، يجد سونغ جين-وو، الصياد المعروف بضعفه، نفسه في صراع لا ينتهي من أجل البقاء. ومع ذلك، بعد حادث غامض في زنزانة مخفية، يحصل على القدرة على 'رفع المستوى'، متحولاً من أضعف صياد إلى قوة لا يمكن إيقافها.",
        "background": "مبني على الرواية الإلكترونية 'Na Honjaman Level Up' التي كتبها تشوجونج. تم نشرها لأول مرة على KakaoPage في عام 2016 وقد اكتسبت شهرة كبيرة على مستوى العالم.",
        "author": {"تشوجونج": "قصة", "DUBU (REDICE STUDIO)": "فن"},
        "type": "Manhwa",
        "start_date": "2018-03-04",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 8.66,  # Example score
        "title_japanese": None,
        "title_english": "Solo Leveling",
        "title_arabic": "رفع المستوي منفردا",
        "title_synonyms": ["I Alone Level Up"]
    }

    solo_leveling_volumes = [
        {"volume_number": 1, "start_chapter": 1, "end_chapter": 16,
         "image": "images/manhwa_images/solo leveling vol 1.jpg"},
        {"volume_number": 2, "start_chapter": 17, "end_chapter": 31,
         "image": "images/manhwa_images/solo leveling vol 2.jpg"},
        {"volume_number": 3, "start_chapter": 32, "end_chapter": 45,
         "image": "images/manhwa_images/solo leveling vol 3.jpg"},
        {"volume_number": 4, "start_chapter": 46, "end_chapter": 59,
         "image": "images/manhwa_images/solo leveling vol 4.jpg"},
        {"volume_number": 5, "start_chapter": 60, "end_chapter": 72,
         "image": "images/manhwa_images/solo leveling vol 5.jpg"},
        {"volume_number": 6, "start_chapter": 73, "end_chapter": 86,
         "image": "images/manhwa_images/solo leveling vol 6.jpg"},
        {"volume_number": 7, "start_chapter": 87, "end_chapter": 98,
         "image": "images/manhwa_images/solo leveling vol 7.jpg"},
        {"volume_number": 8, "start_chapter": 99, "end_chapter": 111,
         "image": "images/manhwa_images/solo leveling vol 8.jpg"},
        {"volume_number": 9, "start_chapter": 112, "end_chapter": 123,
         "image": "images/manhwa_images/solo leveling vol 9.jpg"},
        {"volume_number": 10, "start_chapter": 124, "end_chapter": 134,
         "image": "images/manhwa_images/solo leveling vol 10.jpg"},
    ]

    death_villainess_info = {
        "name": "Death Is the Only Ending for the Villainess",
        "genres": ["الدراما", "الخيال", "الرومانسية", "شوجو"],
        "themes": ["ايسيكاي", "التناسخ", "الشريرة"],
        "demographics": ["شوجو"],
        "synopsis": "بعد أن تستيقظ في جسد الشريرة في لعبتها العثمانية المفضلة، يجب على بينيلوب إيكارت أن تتنقل في عالم حيث يسعى الجميع لقتلها. بهدف البقاء، يجب عليها تجنب علامات الموت من خلال الفوز بمودة أحد الأبطال الذكور.",
        "background": "مبني على رواية ويب شهيرة، 'الموت هو النهاية الوحيدة للشريرة' تم تحويله إلى مانهوا وقد اجتذب القراء بتناوله الفريد لنوع التناسخ.",
        "author": {"غوون غيئول": "قصة", "Suol": "فن"},
        "type": "Manhwa",
        "start_date": "2020-09-18",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 8.39,  # Updated based on MyAnimeList
        "title_japanese": None,
        "title_english": "Death Is the Only Ending for the Villainess",
        "title_arabic": "الموت هو النهاية الوحيدة للشريرة",
        "title_synonyms": ["Villains Are Destined to Die"]
    }

    death_is_the_only_ending_volumes = [
        {"volume_number": 1, "start_chapter": 0, "end_chapter": 31,
         "image": "images/manhwa_images/death is the only ending vol 1.jpg"},
        {"volume_number": 2, "start_chapter": 32, "end_chapter": 53,
         "image": "images/manhwa_images/death is the only ending vol 2.jpg"},
        {"volume_number": 3, "start_chapter": 54, "end_chapter": 73,
         "image": "images/manhwa_images/Death is the only ending for the villainess vol 3.jpg"},
        {"volume_number": 4, "start_chapter": 74, "end_chapter": 93,
         "image": "images/manhwa_images/Death is the only ending for the villainess vol 4.jpg"},
        {"volume_number": 5, "start_chapter": 94, "end_chapter": 113,
         "image": "images/manhwa_images/death is the only ending vol 5.jpg"},
        {"volume_number": 6, "start_chapter": 114, "end_chapter": 129,
         "image": "images/manhwa_images/Death is the only ending for villaines 6.jpg"}
    ]
    how_to_get_husband_info = {
        "name": "How to Get My Husband on My Side",
        "genres": ["الدراما", "الخيال", "الرومانسية", "ايسيكاي"],
        "themes": ["الشريرة", "التناسخ"],
        "demographics": ["شوجو"],
        "synopsis": "تتجسد البطلة كشريرة في عالم خيالي. لتجنب موتها المحتوم، يجب عليها كسب زوجها، الفارس العظيم، من خلال التنقل في العلاقات المعقدة والمكائد السياسية.",
        "background": "مقتبس من رواية ويب شهيرة، تمزج المانهوا عناصر الخيال والرومانسية، وتلتقط القراء بقصتها المعقدة وتطوير الشخصيات.",
        "author": {"جين سويا": "قصة", "Violet": "فن"},
        "type": "Manhwa",
        "start_date": "2021-04-01",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 8.15,  # Example score based on MyAnimeList
        "title_japanese": None,
        "title_english": "How to Get My Husband on My Side",
        "title_arabic": "كيف أجعل زوجي بجانبي",
        "title_synonyms": ["How to Make My Husband on My Side"]
    }
    how_to_get_my_husband_on_my_side_volumes = [
        {"volume_number": 1, "start_chapter": 1, "end_chapter": 10,
         "image": "images/manhwa_images/How to get my husband on my side - 1.jpg"},
        {"volume_number": 2, "start_chapter": 11, "end_chapter": 20,
         "image": "images/manhwa_images/How to get my husband on my side - 2.jpg"},
    ]
    omniscient_reader_info = {
        "name": "Omniscient Reader's Viewpoint",
        "genres": ["الأكشن", "المغامرة", "الخيال", "ايسيكاي"],
        "themes": ["نهاية العالم", "التناسخ"],
        "demographics": ["شونين"],
        "synopsis": "تنقلب حياة كيم دوكجا العادية رأسًا على عقب عندما تصبح الرواية التي كان يقرأها لسنوات، 'ثلاث طرق للبقاء في نهاية العالم'، حقيقة. باعتباره القارئ الوحيد الذي يعرف كيف تتكشف القصة، يجب عليه التنقل في هذا العالم الجديد وتحدياته.",
        "background": "مبني على رواية ويب شهيرة من تأليف سنغ شونغ. وتم استقبال المانهوا بشكل جيد بفضل حبكتها الجذابة وفنها المفصل.",
        "author": {"سنغ شونغ": "قصة", "Sleepy-C": "فن"},
        "type": "Manhwa",
        "start_date": "2020-05-26",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 8.97,  # Example score based on MyAnimeList
        "title_japanese": None,
        "title_english": "Omniscient Reader's Viewpoint",
        "title_arabic": "رؤية القارئ العليم",
        "title_synonyms": ["Omniscient Reader"]
    }

    omniscient_readers_viewpoint_volumes = [
        {"volume_number": 1, "start_chapter": 1, "end_chapter": 15,
         "image": "images/manhwa_images/Omniscient Readers - 1.jpg"},
        {"volume_number": 2, "start_chapter": 16, "end_chapter": 29,
         "image": "images/manhwa_images/Omniscient Readers - 2.jpg"},
        {"volume_number": 3, "start_chapter": 29, "end_chapter": 41,
         "image": "images/manhwa_images/Omniscient Readers - 3.jpg"},
        {"volume_number": 4, "start_chapter": 42, "end_chapter": 53,
         "image": "images/manhwa_images/Omniscient Readers - 4.jpg"},
        {"volume_number": 5, "start_chapter": 54, "end_chapter": 63,
         "image": "images/manhwa_images/Omniscient Readers - 5.jpg"},
        {"volume_number": 6, "start_chapter": 64, "end_chapter": 74,
         "image": "images/manhwa_images/Omniscient Readers - 6.jpg"},
        {"volume_number": 7, "start_chapter": 75, "end_chapter": 84,
         "image": "images/manhwa_images/Omniscient Readers - 7.jpg"},
        {"volume_number": 8, "start_chapter": 85, "end_chapter": 96,
         "image": "images/manhwa_images/Omniscient Readers - 8.jpg"},
        {"volume_number": 9, "start_chapter": 97, "end_chapter": 109,
         "image": "images/manhwa_images/Omniscient Readers - 9.jpg"},
        {"volume_number": 10, "start_chapter": 110, "end_chapter": 123,
         "image": "images/manhwa_images/Omniscient Readers - 10.jpg"}
    ]

    operation_true_love_info = {
        "name": "Operation: True Love",
        "genres": ["الدراما", "الرومانسية", "المدرسة", "شوجو"],
        "themes": ["مضلع الحب", "حياة المدرسة"],
        "demographics": ["شوجو"],
        "synopsis": "تتابع القصة طالبة في المدرسة الثانوية تتنقل في تعقيدات الحب والعلاقات. تنطلق في مهمة لاكتشاف الحب الحقيقي وسط سوء الفهم والتشابكات الرومانسية.",
        "background": "عملية: الحب الحقيقي هو مانها شهير معروف بقصته الرومانسية الجذابة وشخصياته التي يمكن التعاطف معها.",
        "author": {"كوككيو": "قصة", "Durung": "فن"},
        "type": "Manhwa",
        "start_date": None,  # Specific start date not provided
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 8.25,  # Example score based on MyAnimeList
        "title_japanese": None,
        "title_english": "Operation: True Love",
        "title_arabic": "عملية: الحب الحقيقي",
        "title_synonyms": []
    }

    operation_true_love_volumes = [
        {"volume_number": 1, "start_chapter": 0, "end_chapter": 7,
         "image": "images/manhwa_images/Operation true love 1.png"},
        {"volume_number": 2, "start_chapter": 8, "end_chapter": 16,
         "image": "images/manhwa_images/Operation true love 2.png"},
        {"volume_number": 3, "start_chapter": 17, "end_chapter": 23,
         "image": "images/manhwa_images/Operation true love 3.png"},
        {"volume_number": 4, "start_chapter": 24, "end_chapter": 31,
         "image": "images/manhwa_images/Operation true love 4.png"},
        {"volume_number": 5, "start_chapter": 32, "end_chapter": 39,
         "image": "images/manhwa_images/Operation true love 5.png"},
        {"volume_number": 14, "start_chapter": 102, "end_chapter": 108,
         "image": "images/manhwa_images/Operation true love 14.png"},
    ]

    who_made_me_a_princess_info = {
        "name": "Who Made Me a Princess",
        "genres": ["الدراما", "الخيال", "الرومانسية", "ايسيكاي"],
        "themes": ["التناسخ", "الملكية"],
        "demographics": ["شوجو"],
        "synopsis": "تتجسد شابة كأثناسيا، أميرة محكوم عليها بالقتل على يد والدها الإمبراطور في رواية رومانسية. مصممة على البقاء، تستخدم معرفتها بالقصة للتنقل في العالم الخطير للملكية.",
        "background": "مبني على رواية ويب، 'من جعلني أميرة' قد استحوذ على القراء بقصته الجذابة وفنه الجميل.",
        "author": {"بلوتوس": "قصة", "Spoon": "فن"},
        "type": "Manhwa",
        "start_date": "2017-12-20",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 9.03,  # Example score based on MyAnimeList
        "title_japanese": None,
        "title_english": "Who Made Me a Princess",
        "title_arabic": "من جعلني أميرة",
        "title_synonyms": ["Suddenly Became a Princess One Day"]
    }

    who_made_me_a_princess_volumes = [
        {"volume_number": 1, "start_chapter": 1, "end_chapter": 19,
         "image": "images/manhwa_images/Princess - 1.jpg"},
        {"volume_number": 2, "start_chapter": 20, "end_chapter": 35,
         "image": "images/manhwa_images/Princess - 2.jpg"},
        {"volume_number": 3, "start_chapter": 36, "end_chapter": 54,
         "image": "images/manhwa_images/Princess - 3.jpg"},
        {"volume_number": 4, "start_chapter": 55, "end_chapter": 71,
         "image": "images/manhwa_images/Princess - 4.jpg"},
        {"volume_number": 5, "start_chapter": 72, "end_chapter": 88,
         "image": "images/manhwa_images/Princess - 5.jpg"},
        {"volume_number": 6, "start_chapter": 89, "end_chapter": 104,
         "image": "images/manhwa_images/Princess - 6.jpg"},
        {"volume_number": 7, "start_chapter": 105, "end_chapter": 117,
         "image": "images/manhwa_images/Princess - 7.jpg"},
        {"volume_number": 8, "start_chapter": 118, "end_chapter": 126,
         "image": "images/manhwa_images/Princess - 8.jpg"},
    ]
    tears_on_a_withered_flower_info = {
        "name": "Tears on a Withered Flower",
        "genres": ["الرومانسية", "الدراما", "نفسي", "للكبار"],
        "themes": ["الخيانة", "الشفاء"],
        "demographics": ["جوسي"],
        "synopsis": "ينهار عالم نا هاي-سو عندما تكتشف خيانة زوجها، مما يؤدي إلى عواقب مأساوية. بينما تتعامل مع خسارتها، يدخل شاب غامض حياتها، مقدماً فرصة للشفاء وبدايات جديدة.",
        "background": "يستكشف المانهوا موضوعات ناضجة عن الخيانة والنمو الشخصي، مما يتردد مع القراء بسبب عمقه العاطفي وشخصياته المعقدة.",
        "author": {"جاي": "قصة وفن"},
        "type": "Manhwa",
        "start_date": "2024-06-21",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 7.65,  # Example score based on MyAnimeList
        "title_japanese": None,
        "title_english": "Tears on a Withered Flower",
        "title_arabic": "دموع على زهرة ذابلة",
        "title_synonyms": []
    }

    tears_on_withered_flower_volumes = [
        {"volume_number": 1, "start_chapter": 1, "end_chapter": 10,
         "image": "images/manhwa_images/Tears on a withered flower 1.png"},
        {"volume_number": 2, "start_chapter": 11, "end_chapter": 20,
         "image": "images/manhwa_images/Tears on a withered flower 2.png"},
        {"volume_number": 3, "start_chapter": 21, "end_chapter": 31,
         "image": "images/manhwa_images/Tears on a withered flower 3.png"}
    ]

    the_beginning_after_the_end_info = {
        "name": "The Beginning After the End",
        "genres": ["الأكشن", "المغامرة", "الخيال", "ايسيكاي"],
        "themes": ["التناسخ", "السحر"],
        "demographics": ["شونين"],
        "synopsis": "يتجسد الملك جراي، شخصية قوية لا مثيل لها، في عالم مليء بالسحر والوحوش. مسلحًا بتجاربه السابقة، ينطلق ليعيش حياة خالية من الندم وإعادة بناء إرثه.",
        "background": "مبني على رواية ويب كتبها TurtleMe، 'البداية بعد النهاية' قد حظي بالثناء لبناء العالم وتطوير الشخصيات.",
        "author": {"تيرتلمي": "قصة", "Fuyuki23": "فن"},
        "type": "Manhwa",
        "start_date": "2018-07-07",
        "end_date": None,  # As of the latest update
        "favorites": None,  # This would be dynamically updated
        "score": 8.23,  # Example score based on MyAnimeList
        "title_japanese": None,
        "title_english": "The Beginning After the End",
        "title_arabic": "البداية بعد النهاية",
        "title_synonyms": []
    }


the_beginning_after_the_end_volumes = [
    {"volume_number": 1, "start_chapter": 1, "end_chapter": 17,
     "image": "images/manhwa_images/The beginning after the end manhwa - 1 (2).jpg"},
    {"volume_number": 2, "start_chapter": 18, "end_chapter": 34,
     "image": "images/manhwa_images/The beginning after the end manhwa - 2.jpg"},
    {"volume_number": 3, "start_chapter": 35, "end_chapter": 49,
     "image": "images/manhwa_images/The beginning after the end manhwa - 3.jpg"},
    {"volume_number": 4, "start_chapter": 50, "end_chapter": 62,
     "image": "images/manhwa_images/The beginning after the end manhwa - 4.jpg"},
    {"volume_number": 5, "start_chapter": 63, "end_chapter": 77,
     "image": "images/manhwa_images/The beginning after the end manhwa - 5.jpg"},
    {"volume_number": 6, "start_chapter": 78, "end_chapter": 92,
     "image": "images/manhwa_images/The beginning after the end manhwa - 6.jpg"},
    {"volume_number": 7, "start_chapter": 93, "end_chapter": 104,
     "image": "images/manhwa_images/The beginning after the end manhwa - 7.jpg"},
    {"volume_number": 8, "start_chapter": 105, "end_chapter": 115,
     "image": "images/manhwa_images/The beginning after the end manhwa - 8.jpg"},
    {"volume_number": 9, "start_chapter": 116, "end_chapter": 124,
     "image": "images/manhwa_images/The beginning after the end manhwa - 9.jpg"},
    {"volume_number": 10, "start_chapter": 125, "end_chapter": 133,
     "image": "images/manhwa_images/The beginning after the end manhwa - 10.jpg"}
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = [
            (ManhwaData.solo_leveling_info, ManhwaData.solo_leveling_volumes),
            (ManhwaData.death_villainess_info, ManhwaData.death_is_the_only_ending_volumes),
            (ManhwaData.how_to_get_husband_info, ManhwaData.how_to_get_my_husband_on_my_side_volumes),
            (ManhwaData.omniscient_reader_info, ManhwaData.omniscient_readers_viewpoint_volumes),
            (ManhwaData.operation_true_love_info, ManhwaData.operation_true_love_volumes),
            (ManhwaData.who_made_me_a_princess_info, ManhwaData.who_made_me_a_princess_volumes),
            (ManhwaData.tears_on_a_withered_flower_info, ManhwaData.tears_on_withered_flower_volumes),
            (ManhwaData.the_beginning_after_the_end_info, the_beginning_after_the_end_volumes),
        ]

        with atomic():
            for product_info, volumes in products:
                product, _ = Product.objects.get_or_create(**product_info)
                for volume in volumes:
                    Volume.objects.get_or_create(
                        price=Money('12000', 'IQD'),
                        product=product,
                        **volume
                    )

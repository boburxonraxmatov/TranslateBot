TOKEN = '5548343273:AAFVFsgJ3LqFQv_bBvDSxkCwnCJjg39SBL0'

LANGUAGES = {
    'zh-cn': 'Китайский',
    'ru': 'Русский',
    'de': 'Немецкий',
    'en': 'Английский',
    'uz': 'Узбекский',
    'es': 'Испанский'
}


def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k






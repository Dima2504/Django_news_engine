from django.utils.text import slugify
from time import time


def ukr_to_english(text: str) -> str:
    ukr = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    latin = 'a|b|v|h|g|d|e|ye|zh|z|y|i|yi|y|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||yu|ya'.split('|')
    trans_dict = {k: v for k, v in zip(ukr, latin)}
    res = ''
    for ch in text:
        res += trans_dict.get(ch.lower())
    return res


def gen_slug_from_email(email: str) -> str:
    return slugify(email.split('@')[0].lower(), allow_unicode=True) + '-' + str(int(time()))

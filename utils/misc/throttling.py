import sys
from random import randint

from typing import Optional


def generate_num(min_num: Optional[str], max_num: Optional[str],
                 min_default: int = 0, max_default: int = 100) -> int:

    # если не указанно первое число ставим стандартные значения (min_default, max_default)
    if not min_num:
        min_num = min_default
        max_num = max_default
    # добавляем ограничение на самое большое и самое маленькое числа
    elif int(min_num) > sys.maxsize:
        min_num = sys.maxsize
    elif int(min_num) < 0:
        min_num = 0

    # если не указанно второе число ставим, то генерация будет от 0 до первого числа
    # поэтому присваиваем первому числу min_default, а второму -- значение первого
    if not max_num:
        min_num, max_num = min_default, int(min_num)
    # также ограничиваем максимальное и минимальное значения
    elif int(max_num) > sys.maxsize:
        max_num = sys.maxsize
    elif int(max_num) < 0:
        max_num = 0

    # после валидации, не забываем, что нам нужны числа, а не строки
    min_num, max_num = int(min_num), int(max_num)

    # если второе число меньше первого, меняем их местами
    if min_num >= max_num:
        min_num, max_num = max_num, min_num

    # генерируем и возвращаем число
    return randint(min_num, max_num)


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator

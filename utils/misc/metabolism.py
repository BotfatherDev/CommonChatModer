# Модуль формул расчета метаболизма и БЖУ

def metabolism_calculation(gender: str,
                           age: int,
                           height: int,
                           weight: int,
                           activity: float):
    """Расчет уровня метаболизма по заданным параметрам
    gender - пол мужской/женский
    age - возраст, полных лет
    height - рост, см
    weight - вес, кг
    activity - коэффициент уровня активности
    """

    result = 0
    if gender == "male":
        result = (66 + 13.7 * weight + 5 * height - 6.8 * age) * activity
    elif gender == "female":
        result = (655 + 9.6 * weight + 1.8 * height - 4.7 * age) * activity

    return int(result)

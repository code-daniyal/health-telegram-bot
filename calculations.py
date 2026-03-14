
# calculations.py

def calculate_bmi(weight, height_cm):
    """Рассчитывает ИМТ, категорию и дает совет."""
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Недостаточный вес"
        advice = "Стоит немного увеличить калорийность питания."
    elif bmi < 25:
        category = "Норма"
        advice = "Отличная форма! Продолжай так же 💪"
    elif bmi < 30:
        category = "Избыточный вес"
        advice = "Добавь больше активности и контроля питания."
    else:
        category = "Ожирение"
        advice = "Рекомендуется консультация специалиста."

    return round(bmi, 2), category, advice


def calculate_calories(weight, height, age):
    """Рассчитывает норму калорий (формула Миффлина-Сан Жеора для мужчин с коэф. 1.4)."""
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    return int(bmr * 1.4)
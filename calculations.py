
# calculations.py

def calculate_bmi(weight, height_cm):
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
    # Формула Миффлина-Сан Жеора для мужчин (базовый метаболизм)
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    # Умножаем на коэффициент средней активности (1.4)
    total_calories = int(bmr * 1.4)
    
    # Расчет БЖУ (Белки 30%, Жиры 30%, Углеводы 40%)
    # Помни: 1г белка = 4ккал, 1г жира = 9ккал, 1г углевода = 4ккал
    protein = int((total_calories * 0.30) / 4)
    fat = int((total_calories * 0.30) / 9)
    carbs = int((total_calories * 0.40) / 4)
    
    return total_calories, protein, fat, carbs
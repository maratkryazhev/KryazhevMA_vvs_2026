import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

#6
print('#6')
df = pd.read_csv('titanic.csv')
print('Файл загружен!')
print()

#7
print('#7')
n = int(input('Введите n: '))
print('Первые', n, 'строк(-и) таблицы:')
print(df.head(n))
print()

#8
print('#8')
print('Последние 5 строк таблицы:')
print(df.tail(5))
print()

#9
print('#9')
print('Строк и столбцов:', df.shape)
print()

#10
print('#10')
print('Столбцы:', df.columns.tolist())
print()

#11
print('#11')
print('Типы данных:')
print(df.dtypes)
print()

#12
print('#12')
numer = ['PassengerId', 'Age', 'SibSp', 'Parch', 'Fare']
categ = ['Survived', 'Pclass', 'Name', 'Sex', 'Ticket', 'Cabin', 'Embarked']
print('Числовые признаки:', numer)
print('Категориальные признаки:', categ)
print()

#13
print('#13')
stats = df[numer].describe().T
stats['median'] = df[numer].median()
print('Статистика числовых признаков:')
print(stats[['mean', 'median', 'min', 'max', 'std']])
print()

#14
print('#14')
print('Количество пассажиров каждого класса:')
print(df['Pclass'].value_counts().sort_index())
print()

#15
print('#15')
print('Количество уникальных значений в Embarked:', df['Embarked'].nunique())
print()

'''Контрольный вопрос:
Числа 1, 2, 3 - это коды категорий (класс каюты), а не измеряемая величина.
Между ними нет арифметического смысла (нельзя сказать, что 1-й класс "в 3 раза меньше" 3-го).
Поэтому Pclass - категориальный признак.'''

shape_before = df.shape

#16
print('#16')
print('Количество пропусков в каждом столбце:')
print(df.isna().sum())
print()

#17
print('#17')
print('Процент пропусков относительно общего числа строк:')
print((df.isna().mean() * 100).round(2))
print()

#18
print('#18')
print('Максимум пропусков в:', df.isna().sum().idxmax())
print()

#19
print('#19')
age_before = {
    'Среднее': round(float(df['Age'].mean())),
    'Медиана': round(float(df['Age'].median())),
    'Минимум': round(float(df['Age'].min())),
    'Максимум': round(float(df['Age'].max())),
    'Стандартное отклонение': round(float(df['Age'].std())),
    'Кол-во известных значений': round(float(df['Age'].count()))
}
print('Статистика Age до заполнения:')
print(age_before)
print()

#20
print('#20')
median_age = df['Age'].median()
df['Age'] = df['Age'].fillna(median_age)
print('Пропуски в Age заполнены медианой')
print()

#21
print('#21')
age_after = {
    'Среднее': round(float(df['Age'].mean())),
    'Медиана': round(float(df['Age'].median())),
    'Минимум': round(float(df['Age'].min())),
    'Максимум': round(float(df['Age'].max())),
    'Стандартное отклонение': round(float(df['Age'].std())),
    'Кол-во известных значений': round(float(df['Age'].count()))
}
print('Статистика Age после заполнения:')
print(age_after)
print()

#22
print('#22')
comparison = pd.DataFrame({
    'До обработки': age_before,
    'После обработки': age_after
})
print('Сравнительная таблица:')
print(comparison)
print()

#23
print('#23')
df = df.dropna(subset=['Embarked'])
print('Все строки без Embarked удалены')
print()

#24
print('#24')
cabin_missing_share = df['Cabin'].isna().mean()
print('Доля пропусков в Cabin:', round(cabin_missing_share * 100, 2), '%')
if cabin_missing_share > 0.5:
    df = df.drop(columns=['Cabin'])
    print('Столбец Cabin удалён, так как доля пропусков превысила 50%')
print()

#25
print('#25')
print('Оставшиеся пропуски:')
print(df.isna().sum())
print()

#26
print('#26')
print('Размер до обработки:', shape_before)
print('Размер после обработки:', df.shape)
print()

'''Контрольные вопросы:
#27. Медиана более устойчива к выбросам и сильной асимметрии распределения.
А среднее «тянется» к выбросам, которых в Age достаточно.
#28. Не изменились: медиана, минимум, максимум.
Изменились: стандартное отклонение (уменьшилось), кол-во известных значений (стало равно числу строк).
Визуально среднее не изменилось из-за округления, но на самом деле немного сдвинулось к медиане.
#29. Все добавленные значения равны медиане, поэтому они сжимают разброс.
Таким образом они уменьшают стандартное отклонение.
#30. Нет, распределение искажается, так как появляется искусственный «пик» на медиане.
Заполнение медианой не восстанавливает исходную форму распределения.'''

#31
print('#31')
survived = df['Survived'].to_numpy()
print('Общий процент выживших:', round(survived.mean() * 100, 2), '%')
print()

#32
print('#32')
for sex in ['male', 'female']:
    mask = (df['Sex'].to_numpy() == sex)
    print(f"Процент выживших среди {sex}: {round(survived[mask].mean() * 100, 2)}%")
print()

#33
print('#33')
age = df['Age'].to_numpy()
for sex in ['male', 'female']:
    mask = (df['Sex'].to_numpy() == sex)
    print(f"Средний возраст {sex}: {round(age[mask].mean(), 2)}")
print()

#34
print('#34')
for sex in ['male', 'female']:
    for s in [0, 1]:
        mask = (df['Sex'].to_numpy() == sex) & (survived == s)
        label = 'выживших' if s == 1 else 'погибших'
        ages_in_group = age[mask]
        if len(ages_in_group) > 0:
            print(f"Среди {sex} {label}: {round(age[mask].mean(), 2)}")
        else:
            print(f"Среди {sex} {label}: нет данных (0 человек)")
print()

#35
print('#35')
print('Минимальная стоимость билета:', round(df['Fare'].min(), 2))
print('Максимальная стоимость билета:', round(df['Fare'].max(), 2))
print('Средняя стоимость билета:', round(df['Fare'].mean(), 2))
print()

#36
print('#36')
print('Стандартное отклонение возраста:', round(age.std(), 2))
print()

data = {
    'Мужчины': ['0.0%', '29.52', 'нет данных (0 чел.)', '29.52'],
    'Женщины': ['100.0%', '29.73', '29.73', 'нет данных (0 чел.)']
}
index = ['Процент выживших', 'Средний возраст', 'Ср. возраст выживших', 'Ср. возраст погибших']
comparative_df = pd.DataFrame(data, index=index)
print('Сравнительная таблица по полу:')
print(comparative_df)
print()

'''Контрольный вопрос:
В данном наборе данных наблюдается кардинальное различие в выживаемости:
выжили только женщины (100% выживаемость), в то время как все мужчины погибли.
Средний возраст выживших женщин составляет примерно 29.73 года.
Из-за того, что в файле нет выживших мужчин и погибших женщин,
сравнить их средний возраст не представляется возможным.'''

# Фильтрация данных. Начало
#1
print('Фильтрация. Задание 1')
task1 = df[(df['Sex'] == 'male') & (df['Age'] > 30) & (df['Pclass'] == 1)]
print('Число пассажиров:', len(task1))
print('Первые 10 строк результата:')
print(task1.head(10))
print()

#2
print('Фильтрация. Задание 2')
task2 = df[((df['Age'] < 18) | (df['Sex'] == 'female')) & (df['Survived'] == 1)]
print('Число пассажиров:', len(task2))
print()

#3
print('Фильтрация. Задание 3')
mean_fare_3 = df[df['Pclass'] == 3]['Fare'].mean()
task3 = df[(df['Pclass'] == 3) & (df['Fare'] > mean_fare_3)]
print('Средняя стоимость билета в 3-м классе:', round(mean_fare_3, 2))
print('Число пассажиров:', len(task3))
print('Пассажиры:')
print(task3.head())
print()

#4
print('Фильтрация. Задание 4')
task4 = df[(df['Age'] >= 20) & (df['Age'] <= 40) & (df['Embarked'] == 'S')]
print('Число пассажиров:', len(task4))
print('Пассажиры:')
print(task4.head())
print()
# Фильтрация данных. Конец

#37
print('#37')
group_and_sex_stats = df.groupby(['Pclass', 'Sex']).agg(
    count=('PassengerId', 'count'),
    mean_age=('Age', 'mean'),
    survival_rate=('Survived', lambda x: round(x.mean() * 100, 2)),
    mean_fare=('Fare', 'mean')
)
print('Группировка по классу и полу:')
print(group_and_sex_stats)
print()

#38
print('#38')
embarked_stats = df.groupby('Embarked').agg(
    count=('PassengerId', 'count'),
    survival_rate=('Survived', lambda x: round(x.mean() * 100, 2))
)
print('Группировка по порту посадки:')
print(embarked_stats)
print()

#39
print('#39')
survival_by_class = df.groupby('Pclass')['Survived'].mean()
print('Кол-во выживших по классам:')
print(survival_by_class)
print('Класс с наибольшей долей выживших:', survival_by_class.idxmax())
print()

#40
print('#40')
df.to_csv('titanic_processed.csv', index=False)
print('Обработанный DataFrame сохранён')
print()

#41
print('#41')
group_and_sex_stats.to_csv('titanic_statistics.csv')
print('Результаты группировки по классу и полу сохранены')
print()

#42
print('#42')
check = pd.read_csv('titanic_processed.csv')
print('Размер загруженного файла:', check.shape)
print('Совпадает с исходным:', check.shape == df.shape)
      
'''Выводы по работе:
#43. Наибольшее количество пропусков содержал признак Cabin (327 пропусков, 78.23% от всех данных).
На втором месте по количеству пропусков находился признак Age (86 пропусков, 20.57% от всех данных).
#44. В связи с тем, что доля пропусков в Cabin превысила 50%,
данный столбец был удален, поэтому количество столбцов уменьшилось с 12 до 11.
Количество строк осталось прежним (418), так как в используемом файле не было пропусков в Embarked.
Заполнение пропусков в Age медианой (27 лет) увеличило количество известных значений с 332 до 418.
При этом медиана (27), минимум (0) и максимум (76) не изменились.
Среднее значение визуально осталось на уровне 30 (из-за округления),
а стандартное отклонение уменьшилось с 14 до 13, так как новые значения сгруппировались вокруг медианы.
#45. В данном наборе данных выживаемость различалась кардинально: выжили 100% женщин и 0% мужчин.
Общая доля выживших составила 36.36%. Из-за такой специфики выборки средний возраст погибших (29.52) совпал
со средним возрастом всех мужчин, а средний возраст выживших (29.73) - со средним возрастом всех женщин.
#46. Наибольшая доля выживших наблюдалась в 1-м классе (46.73%).
Во 2-м и 3-м классах выживаемость была значительно ниже и составила 32.26% и 33.03% соответственно.
#47. В Pandas наиболее полезными оказались функции загрузки данных (read_csv),
исследования структуры (shape, columns, dtypes), обработки пропусков (isna, fillna, dropna),
а также инструмент группировки и агрегации данных (groupby и agg).
В NumPy крайне полезными оказались методы преобразования столбцов в массивы (to_numpy)
и векторные вычисления с использованием логических масок (например, для быстрого расчета средних значений
возраста и процентов выживаемости отдельно для мужчин и женщин без использования циклов).'''

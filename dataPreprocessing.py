import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

# Функция для определения дня недели по значению dateTime
def date_convert(date_to_convert):
     return datetime.strptime(date_to_convert, "%Y-%m-%d %H:%M:%S").weekday()

# Функция для определения часа по значению dateTime
def hour_convert(date_to_convert):
     return datetime.strptime(date_to_convert, "%Y-%m-%d %H:%M:%S").time().hour

# Рассматриваемые даты
start_date = date(2021, 5, 15)
end_date = date(2021, 6, 15)
proc_date = start_date
delta = timedelta(days=1)

drop_columns = ['dateTime', 'campaign', 'campaignType', 'spot', 'banner', 'uid',
    'ip', 'affiliateNetwork', 'path', 'ua', 'action', 'convType', 'convPayout', 'isp']

dataset = pd.DataFrame()
dataset_cut = pd.DataFrame()
dataset_fragm = pd.DataFrame()

# Цикл обработки файлов по датам
while proc_date <= end_date:

    proc_date_str = proc_date.strftime('%Y-%m-%d')
    dataset_fragm = pd.read_csv('E:/Work/RTB/forGit/data/revenue_'+
        proc_date_str + '.csv')

    # Замена отсутствующих значений нулями
    dataset_fragm = dataset_fragm.fillna(0)
    # Добавление колонки с днями недели для каждой записи
    dataset_fragm['weekday'] = dataset_fragm.dateTime.apply(date_convert)
    # Добавление колонки с часами для каждой записи
    dataset_fragm['hour'] = dataset_fragm.dateTime.apply(hour_convert)
    # Удаление ненужных колонок
    dataset_fragm = dataset_fragm.drop(drop_columns, axis=1)

    # Создание урезанной версии обучающей выборки с более равномерным
    # распределением данных по доходам
    data_rev_1 = dataset_fragm.loc[dataset_fragm['revenue'] != 0]
    data_rev_0 = dataset_fragm.loc[dataset_fragm['revenue'] == 0]
    size_rev_data = len(data_rev_1.index)
    data_rev_0_cut = data_rev_0.sample(n = size_rev_data)

    # Датасеты для решение задачи регрессии
    # dataset_class - выборка, в которой получилось значительно больше записей с
    # нулевым доходом, чем записей с положительным доходом,
    # dataset_cut - урезанная выборка
    dataset_cut = pd.concat([dataset_cut, data_rev_1, data_rev_0_cut])
    dataset = pd.concat([dataset, dataset_fragm])

    proc_date += delta

# Датасеты для решения задачи классфикации
dataset_class = dataset.copy(deep=True)
dataset_class.loc[dataset_class['revenue'] > 0, 'revenue'] = 1
dataset_class['revenue'] = dataset_class['revenue'].map(int)

dataset_cut_class = dataset_cut.copy(deep=True)
dataset_cut_class.loc[dataset_cut_class['revenue'] > 0, 'revenue'] = 1
dataset_cut_class['revenue'] = dataset_cut_class['revenue'].map(int)

# Сохранение данных в csv-файлы
dataset_cut.to_csv('dataset_cut.csv', index=False)
dataset.to_csv('dataset.csv', index=False)
dataset_cut_class.to_csv('dataset_cut_class.csv', index=False)
dataset_class.to_csv('dataset_class.csv', index=False)

print("Done")

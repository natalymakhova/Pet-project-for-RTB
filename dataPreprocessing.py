import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta

# Функция для определения дня недели по значению dateTime
def dateConvert(date_to_convert):
     return datetime.strptime(date_to_convert, "%Y-%m-%d %H:%M:%S").weekday()

# Функция для определения часа по значению dateTime
def hourConvert(date_to_convert):
     return datetime.strptime(date_to_convert, "%Y-%m-%d %H:%M:%S").time().hour

def prepData(dataset_fragm):
    dataset_fragm = dataset_fragm.fillna(0)
    dataset_fragm['weekday'] = dataset_fragm.dateTime.apply(dateConvert)
    dataset_fragm['hour'] = dataset_fragm.dateTime.apply(hourConvert)
    dataset_fragm = dataset_fragm.drop(drop_columns, axis=1)
    return dataset_fragm

def  makeCutData(dataset_fragm, dataset_cut):
        # Создание урезанной версии обучающей выборки с более равномерным
        # распределением данных по доходам
        data_rev_1 = dataset_fragm.loc[dataset_fragm['revenue'] != 0]
        data_rev_0 = dataset_fragm.loc[dataset_fragm['revenue'] == 0]
        size_rev_data = len(data_rev_1.index)
        data_rev_0_cut = data_rev_0.sample(n = size_rev_data)
        dataset_cut = pd.concat([dataset_cut, data_rev_1, data_rev_0_cut])
        return dataset_cut

def makeClassData(dataset):
    dataset_class = dataset.copy(deep=True)
    dataset_class.loc[dataset_class['revenue'] > 0, 'revenue'] = 1
    dataset_class['revenue'] = dataset_class['revenue'].map(int)
    return dataset_class

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
    # Замена NaN нулями, добавление и удаление колонок
    dataset_fragm = prepData(dataset_fragm)

    dataset = pd.concat([dataset, dataset_fragm])
    dataset_cut =  makeCutData(dataset_fragm, dataset_cut)
    proc_date += delta

# Датасеты для решения задачи классфикации
dataset_class = makeClassData(dataset)
dataset_cut_class = makeClassData(dataset_cut)

# Сохранение данных в csv-файлы
dataset_cut.to_csv('dataset_cut.csv', index=False)
dataset.to_csv('dataset.csv', index=False)
dataset_cut_class.to_csv('dataset_cut_class.csv', index=False)
dataset_class.to_csv('dataset_class.csv', index=False)

print("Done")

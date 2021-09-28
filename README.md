# Pet-project-for-RTB
**RTB - Real Time Bidding, или торг в реальном времени. 
В данном проекте осущствляется обработка и анализ данных, собранных в RTB-системе.** 

## Задача 
По данным пользователя с некоторой долей вероятности определить, принесет ли данный пользователь положительный доход. 

*Данный проект является демонстрационным, однако он может стать основой для системы RTB, которая самостоятельно выбирает размер ставок, используя для этого накопленные данные и алгоритмы машинного обучения.* 

## Данные 
В наличии имеется несколько репозиториев с файлами, которые находятся на FTP-сервере. 
Данные представляют собой архивы двух типов: 
- данные с показами;
- данные с "кликами".
В первых содержится информация о показанной рекламе и пользователях, которые эту рекламу увидели. 
Во вторых - иформация, относящаяся к случаям, когда пользователь не только увидел рекламу, но и кликнул на рекламный баннер. Если после клика на баннер была осуществлено целевое действие, приносящее рекламодателю доход, то такой пользователь имеет положительное число в графе "revenue" (доход).

## Файлы проекта

### DataAnalysis.ipynb 
	Имеющиейся файлы с данными рассматриваются с целью определить их содержание и характер хранящихся там данных. 
	
### getData.py 
	Файлы скачиваются поочередно и рассматриваются фрагментами, поскольку файлы с показами содержат около 120 миллионов записей, файлы с кликами - около 1,5 миллионов. Набранные в процессе обработки данные сохраняются для дальнешей работы. 

### dataPreprocessing.py
	Обработка данных и создания обучающих выборок.

### ML_Regression.ipynb 
	Решение задачи регрессии, где в качестве целевой функции выступает графа "доход" (revenue). Обученная модель должена определить, какой доход (revenue) можно ждать от определенного пользователя.
  Использованные для обучения алгоритмы: Random Forest, XGBoost

### ML_Classification.ipynb 
	Решение задачи классификации, где в качестве целевой функции выступает графа "доход" (revenue).
Классификатор должен определить, будет ли от определенного пользователя, кликнувшего рекламу доход (revenue=1) , или нет (revenue=0).
Использованные для обучения алгоритмы: Random Forest, XGBoost
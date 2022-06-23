# Pet-project-for-RTB
**RTB - Real Time Bidding. 
The project analyzes the data of site visitors.** 

## Project Description
The data for the project was obtained from a real advertising platform. The first step was to identify users who clicked on an advertising link and were more likely to generate income. Also, from this data, you can get information about the fraud and which users should be shown ads in principle. These are the next steps.
The ultimate goal is to develop an RTB system that independently chooses the size of bets using accumulated data and machine learning algorithms.

## Data Description
There are several repositories with files that are located on the FTP server.
The data are archives of two types:
- data with impressions;
- data with "clicks".
The first contains information about the ad shown and the users who saw this ad.
Secondly, information related to cases when the user not only saw an advertisement, but also clicked on an advertising banner. If, after clicking on the banner, a target action was performed that brought the advertiser income, then such a user has a positive number in the "revenue" (income) column.

## Project files

### DataAnalysis.ipynb 
Data files are reviewed to determine their content and the nature of the data stored there.
	
### getData.py 
Files are downloaded one by one and considered as fragments, since files with impressions contain about 120 million records, files with clicks - about 1.5 million. The data collected during processing is stored for further work.

### dataPreprocessing.py
Data processing and creation of training samples.

### ML_Regression.ipynb 
The solution of the regression problem, where the "income" column (revenue) acts as the objective function. The trained model must determine what revenue (revenue) can be expected from a particular user.
Algorithms used for training: Random Forest, XGBoost

### ML_Classification.ipynb 
The solution of the classification problem, where the "income" column (revenue) acts as the objective function.
The classifier must determine whether a certain user who clicks on an ad will generate income (revenue=1) or not (revenue=0).
Algorithms used for training: Random Forest, XGBoost

import pandas as pd
import numpy as np
import os
import py7zr
import ftplib
from datetime import date, timedelta
import time

def filesName(proc_date):
    proc_date_str = proc_date.strftime('%Y-%m-%d')
    file_name_7z = proc_date_str +'.7z'
    file_name_clc = proc_date_str +'-clc'+'.csv'
    file_name_imp = proc_date_str +'-imp'+'.csv'
    return proc_date_str, file_name_7z, file_name_clc, file_name_imp

def downloadFile(file_name_7z, folder_name, new_file_name):
    ftp.cwd('/'+folder_name)
    ftp.retrbinary('RETR '+file_name_7z, open(file_name_7z, 'wb').write)
    # Извлечение архива
    with py7zr.SevenZipFile(file_name_7z, mode='r') as z:
        z.extractall()
    os.rename(proc_date_str+".csv", new_file_name)
    # Удаление исходного архива
    os.remove(file_name_7z)
    ftp.cwd('..')

def firstClcProcessing(file_name_clc):
    df_clicks = pd.read_csv(file_name_clc)
    df_clicks[columns] = df_clicks[columns].astype(object, errors = 'raise')
    df_clicks = df_clicks.drop(['date', 'spot', 'banner', 'bannerSize', 'ua', 'isp',
        'browserVersion', 'osVersion', 'deviceModel', 'deviceBrand',
        'affiliateNetwork', 'connType', 'proxyType'], axis=1)
    return df_clicks

def concatClcFragments(df_clicks):
    click_revenue_1 = df_clicks.loc[df_clicks['convType'].notnull()]
    click_revenue_0 = df_clicks.loc[df_clicks['convType'].isnull()]
    click_revenue_0_small = click_revenue_0.sample(n = 5000)
    for_revenue_file = pd.concat([click_revenue_1, click_revenue_0_small])
    for_revenue_file.to_csv('revenue_' + proc_date_str + '.csv', index=False)
    click_revenue_0 = click_revenue_0.sample(n = 40000)
    click_main = pd.concat([click_revenue_1, click_revenue_0])
    return for_revenue_file, click_main


chunk_size = 10000         # The size of the processed fragments
impressions_folder = '3'   # The name of the folder containing the impressions
click_folder = '4'         # The name of the folder containing the clicks
df_main = pd.DataFrame()
gap = 10000000             # The size of the fragment that is processed between
                            # displaying information on the screen
# Column names whose data type needs to be changed
columns = ['date', 'dateTime', 'campaign', 'campaignType', 'spot', 'banner',
       'bannerSize', 'uid', 'language', 'ip', 'country', 'city', 'browser',
       'browserVersion', 'os', 'osVersion', 'deviceType', 'deviceModel',
       'deviceBrand', 'trafficSource', 'affiliateNetwork', 'offer', 'path',
       'ua', 'connType', 'proxyType']
# The names of the columns, according to the values of which the data from the
# files are combined with impressions and clicks
columns_cut = ['dateTime', 'uid', 'language', 'ip', 'country', 'city', 'browser',
    'os', 'deviceType']

# Entering data for the server
ftp_server = input('Enter Host: ')
username = input('Enter Username:')
passv = input('Enter Password: ')
# Directory for saved files
save_dir = input('Save directory: ')

# Processed dates
start_date = date(2021, 5, 15)
end_date = date(2021, 5, 15)
proc_date = start_date
delta = timedelta(days=1)

os.chdir(save_dir)

# A loop that processes files with impressions and clicks one by one
# for each date from the given interval
while proc_date <= end_date:
    start_time = time.time()    # Начало отсчета времени
    proc_date_str, file_name_7z, file_name_clc, file_name_imp = filesName(proc_date)

    # Connecting to an FTP server
    ftp = ftplib.FTP(ftp_server)
    ftp.login(username, passv)
#  Downloading data files
    print("---Download file", file_name_7z, "from click folder")
    downloadFile(file_name_7z, click_folder, file_name_clc)

    print("---Download file", file_name_7z, "from impression folder")
    downloadFile(file_name_7z, impressions_folder, file_name_imp)

    print('---Processing ', proc_date_str)
    # Loading and processing a file with clicks
    df_clicks = firstProcessing(file_name_clc)

    # A set of random data from subsamples with and without rhubarb
    for_revenue_file, click_main = concatClcFragments(df_clicks)
    for_revenue_file.to_csv('revenue_' + proc_date_str + '.csv', index=False)

    finded_records_df = pd.DataFrame()
    impressions_data = pd.DataFrame()
    count_chunks = 0

    # Step-by-step processing of a file with impressions
    for chunk in pd.read_csv(file_name_imp, usecols=columns, chunksize=chunk_size):
        chunk[columns] = chunk[columns].astype(object, errors = 'raise')
        chunk = chunk.drop(['date', 'affiliateNetwork'], axis=1)

        # Selecting a random string from a fragment with impressions and adding
        # it to the selection
        random_samples = chunk.sample(n = 50)
        check_if_contains = random_samples.loc[~((random_samples['dateTime'].isin(df_clicks['dateTime']))
            & (random_samples['ip'].isin(df_clicks['ip'])))]
        impressions_data = impressions_data.append(check_if_contains.iloc[0:1,:])
        # Combining overlapping data from a fragment with impressions and typed values
        # from selection with clicks
        contained_rec = chunk.merge(click_main, on = columns_cut, how='inner')

        if not contained_rec.empty:
            finded_records_df = pd.concat([finded_records_df, contained_rec])

        if (chunk_size*(count_chunks+1) % gap) == 0 :
            print(chunk_size*(count_chunks+1)/gap)

        count_chunks += 1

    #  Saving generated data files
    finded_records_df.to_csv('click_data_'+proc_date_str +'.csv', index=False)
    impressions_data.to_csv('impressions_data_'+proc_date_str +'.csv', index=False)

    os.remove(file_name_clc)
    os.remove(file_name_imp)

    proc_date += delta
    # The time it took to process the data relating to the date in question
    print("--- %s min ---" % (np.around((time.time() - start_time)/60, decimals=2)))
    print(" -----------------------------")

print("Done")

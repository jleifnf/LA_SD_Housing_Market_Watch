import pandas as pd
import numpy as np
import re
import csv
import os


def compile_csv(data_path=None):
    if data_path is None:
        proj_path = os.getcwd().replace('/codes', '')
        data_path = os.path.join(proj_path, 'data')
    csv_files = list(filter(re.compile('Full').match, sorted(os.listdir(data_path))))

    cols_tokeep = ['Matrix_Unique_ID', 'CountyOrParish', 'OnMarketDate',
                   'CloseDate', 'CumulativeDaysOnMarket', 'ListPrice', 'ClosePrice']

    dfs = []
    for file in csv_files:
        filename = os.path.join(data_path, file)
        df = pd.read_csv(filename, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                         usecols=cols_tokeep, header=0, low_memory=False)
        dfs.append(df)
    mls_df = pd.concat(dfs, ignore_index=True)
    mls_df = mls_df.drop_duplicates(subset='Matrix_Unique_ID', keep='first')
    return mls_df


def data_preprocessing(df):
    df.CloseDate = pd.to_datetime(df.CloseDate)
    df.OnMarketDate = pd.to_datetime(df.OnMarketDate)
    df = df.sort_values(by='CloseDate')
    df.CloseDate = df.CloseDate.where((df.CloseDate.dt.year > 2014)
                                      & (df.CloseDate.dt.year < 2020))

    df = df.dropna().sort_values(by='CloseDate')

    df['CloseYearWeek'] = df.CloseDate.apply(datetime_to_weekofyear)

    df['PriceDifference'] = df.ClosePrice - df.ListPrice
    df['PriceRatio'] = df.ClosePrice / df.ListPrice
    df['PriceDiffRatio'] = (df.ClosePrice - df.ListPrice) / df.ListPrice

    df = df[(df.PriceRatio < 2) & (df.PriceDiffRatio > -0.95)]

    df['OnMarketDays'] = df.CloseDate - df.OnMarketDate
    df.OnMarketDays = df.OnMarketDays.dt.days.astype('int64')

    return df


def datetime_to_weekofyear(datetime):
    if int(datetime.dayofyear) > 358 and int(datetime.weekofyear) == 1:
        return str(datetime.year) + ' - ' + str(53)
    else:
        return str(datetime.year) + ' - ' + str(datetime.weekofyear)

# mls_df = compile_csv()
# mls_df = data_preprocessing(mls_df)

import pandas as pd
import numpy as np
import re
import csv
import os


def datetime_to_weekofyear(datetime):
    if int(datetime.dayofyear) > 358 and int(datetime.weekofyear) == 1:
        return str(datetime.year) + ' - ' + str(53)
    elif int(datetime.weekofyear) < 10:
        return str(datetime.year) + ' - 0' + str(datetime.weekofyear)
    else:
        return str(datetime.year) + ' - ' + str(datetime.weekofyear)


def compile_csv(data_path=None):
    if data_path is None:
        proj_path = os.getcwd().replace('/codes', '')
        data_path = os.path.join(proj_path, 'data')
    csv_files = list(filter(re.compile('Full').match, sorted(os.listdir(data_path))))

    cols_tokeep = ['Matrix_Unique_ID', 'CountyOrParish', 'OnMarketDate',
                   'CloseDate', 'ListPrice', 'ClosePrice']

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

    df['OnMarketDays'] = df.CloseDate - df.OnMarketDate
    df.OnMarketDays = df.OnMarketDays.dt.days.astype('int64')

    for col in ['ClosePrice', 'ListPrice', 'OnMarketDays']:
        df = df[df[col] < df[col].quantile(0.99)]

    df['CloseYearWeek'] = df.CloseDate.apply(datetime_to_weekofyear)

    df['PriceDifference'] = df.ClosePrice - df.ListPrice
    df['PriceRatio'] = df.ClosePrice / df.ListPrice
    df['PriceDiffRatio'] = (df.ClosePrice - df.ListPrice) / df.ListPrice

    df = df[(df.PriceRatio < 2) & (df.PriceDiffRatio > -0.95)]

    df = df[df.OnMarketDays > 0]
    df.CountyOrParish = pd.Categorical(df.CountyOrParish)
    df.CloseYearWeek = pd.Categorical(df.CloseYearWeek)

    df['SixtyDays'] = df.OnMarketDays.map(lambda x: '> 60 days' if x > 60 else '< 60 days')

    return df


def CLT_bootstrap(df, n_times=200, n_samples=1000):
    """ Returns the dataframe with only the variables of interest """
    rs = np.random.RandomState(seed=2020)
    means = [pd.DataFrame(df.sample(n_samples, replace=True, random_state=rs).mean()).T for i in range(n_times)]
    return pd.concat(means)

# mls_df = compile_csv()
# mls_df = data_preprocessing(mls_df)

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
    dfs = []
    for file in csv_files:
        filename = os.path.join(data_path, file)
        df = pd.read_csv(filename, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                         header=0, low_memory=False)
        dfs.append(df)
    mls_df = pd.concat(dfs, ignore_index=True)
    return mls_df

# mls_df = compile_csv()
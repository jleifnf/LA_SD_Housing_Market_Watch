""" Look through downloaded MLS data and combine into a single CSV file. """
import csv
import os
import pandas as pd
import re
import numpy as np


def read_listings(fName):
    mlsDB = pd.read_csv(fName, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                        header=0, low_memory=False)
    #
    list_agent_cols = list(filter(re.compile('ListAgent').match, mlsDB.columns))
    buyer_agent_cols = list(filter(re.compile('BuyerAgent').match, mlsDB.columns))
    text_cols = ['PublicRemarks', 'PrivateRemarks',
                 'SyndicationRemarks', 'ShowingInstructions']
    mlsDB[list_agent_cols + buyer_agent_cols + text_cols] = ''
    #
    return mlsDB


rootPath = os.getcwd()
projPath = os.path.join(rootPath, 'mls_csv')
df = []
xlsFiles = list(filter(re.compile('Full').match, sorted(os.listdir(projPath))))
if len(xlsFiles) > 0:
    for file in xlsFiles:
        filename = os.path.join(projPath, file)
        df.append(read_listings(filename))
    mlsDB = pd.concat(df, ignore_index=True)
    mlsDB = mlsDB.drop_duplicates(subset='Matrix_Unique_ID', keep='first')
    segments = np.array_split(mlsDB, round(mlsDB.shape[0] / 5e3) + 1, axis=0)
    for i, df in enumerate(segments):
        df.to_csv(os.path.join(projPath, f'Full_{i}.csv'), sep=',',
                  quoting=csv.QUOTE_MINIMAL, header=mlsDB.columns, index=False)

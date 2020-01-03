""" Look through downloaded MLS data and combine into a single CSV file. """
import csv, pandas as pd, os, re
from multiprocessing import Pool


# past 575 days from 10/27/19 for:
# Temple City, West Covina, Rosemead/S-San Gabriel, Arcadia [605,651,661,669]
# 15 days from 10/27/19 from Fontana, Alhambra, Diamond Bar, El Monte [264,601,616,619]
# ('Single Family Residence', 'Condominium', 'Townhouse',)
# *** all area for the 12 days ago from 10/29/19

def readListings(fName):
    mlsDB = pd.read_csv(fName, delimiter=',', quoting=csv.QUOTE_MINIMAL,
                        header=0, low_memory=False)
    return mlsDB


rootPath = os.getcwd()
for folder in ['la_mls_csv', 'sd_mls_csv']:
    projPath = os.path.join(rootPath, folder)
    df = []
    xlsFiles = list(filter(re.compile('Full').match, sorted(os.listdir(projPath))))
    if len(xlsFiles) > 0:
        for file in xlsFiles:
            filename = os.path.join(projPath, file)
            df.append(readListings(filename))
        mlsDB = pd.concat(df, ignore_index=True)
        mlsDB = mlsDB.drop_duplicates(subset='Matrix_Unique_ID', keep='first')
        mlsDB.to_csv(os.path.join(projPath, 'Full (0).csv'), sep=',', header=mlsDB.columns, index=False)

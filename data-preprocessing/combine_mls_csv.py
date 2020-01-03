""" Look through downloaded MLS data and combine into a single CSV file. """
import csv, pandas as pd, os, re
from multiprocessing import Pool


# past 575 days from 10/27/19 for:
# Temple City, West Covina, Rosemead/S-San Gabriel, Arcadia [605,651,661,669]
# 15 days from 10/27/19 from Fontana, Alhambra, Diamond Bar, El Monte [264,601,616,619]
# ('Single Family Residence', 'Condominium', 'Townhouse',)
# *** all area for the 12 days ago from 10/29/19

def readListings(fNo):
    mlsDB = pd.read_csv(os.path.join(projPath, 'Full (%s).csv' % fNo), delimiter=',', quoting=csv.QUOTE_MINIMAL,
                        header=0, low_memory=False)
    return mlsDB

rootPath = os.getcwd()
projPath = os.path.join(rootPath,'mls_csv')

xlsFiles = list(filter(re.compile('Full').match, sorted(os.listdir(projPath))))
pool = Pool(int(max([min([len(xlsFiles) / 10, 4]), 1])))
mlsDB = pool.map(readListings, range(0, len(xlsFiles)))
mlsDB = pd.concat(mlsDB, ignore_index=True)
mlsDB = mlsDB.drop_duplicates(subset='Matrix_Unique_ID', keep='first')
mlsDB.to_csv(os.path.join(projPath, 'Full (0).csv'), sep=',', header=mlsDB.columns, index=False)
pool.close()


import glob
import os
import pandas as pd
import re

def merge():
    files = glob.iglob("/Users/akshaybhoge/PycharmProjects/StockAPI/data/Stocks/*", recursive=True)
    filesETFs = glob.iglob("/Users/akshaybhoge/PycharmProjects/StockAPI/data/ETFs/*", recursive=True)
    li = []
    for file in files:
        if os.stat(file).st_size > 0:
            df = pd.read_csv(file, delimiter=',', header=None, skiprows=1)
            (dirname, filename) = os.path.split(file)
            (shortname, extension) = os.path.splitext(filename)
            shortname = re.split(r'\.(?!\d)', shortname)
            # print(shortname, extension)
            df['Company'] = shortname[0]
            df['ETFs/Stocks'] = 'Stocks'
            li.append(df)
        else:
            continue
    for file in filesETFs:
        if os.stat(file).st_size > 0:
            df = pd.read_csv(file, delimiter=',', header=None, skiprows=1)
            (dirname, filename) = os.path.split(file)
            (shortname, extension) = os.path.splitext(filename)
            shortname = re.split(r'\.(?!\d)', shortname)
            # print(shortname, extension)
            df['Company'] = shortname[0]
            df['ETFs/Stocks'] = 'ETF'
            li.append(df)
        else:
            continue

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.columns = ["Date", "open", "High", "Low", "close", "Volume", "Openint", "Company", 'ETFs/Stocks']
    print(frame)
    frame.to_csv(r'/Users/akshaybhoge/PycharmProjects/StockAPI/data/datanew.csv', index = False)

#merge()

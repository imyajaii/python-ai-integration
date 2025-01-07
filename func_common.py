import pandas as pd

CSV_FILE_PATH_TH_DOMESTIC_TOUR = 'data/thailand_domestic_tourism.csv'
CSV_FILE_PATH_TH_DOMESTIC_TOUR_ORG = 'data/thailand_domestic_tourism_original.csv'

# Load CSV data into a DataFrame
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(e)

# Load Thailand domestic tourism
def load_domestic_tourist_csv():
    return load_csv(CSV_FILE_PATH_TH_DOMESTIC_TOUR)

# Load Thailand domestic tourism original file
def load_domestic_tourist_org_csv():
    return load_csv(CSV_FILE_PATH_TH_DOMESTIC_TOUR_ORG)

def billions_formatter(y, pos):
    return "{:,}B".format(int(y/1e9))

def millions_formatter(y, pos):
    return f'{int(y/1e6)}M'

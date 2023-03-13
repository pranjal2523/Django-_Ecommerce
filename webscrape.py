#import requests
#from bs4 import beautifulSoap as bs4
import pandas as pd
SHEET_ID = '1QQj8gAD9jexgz2OoYEyQOIe7xVSG-0r0FyTDHSAYYg0'
SHEET_NAME = 'AAPL'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}'
df = pd.read_csv(url)
print(df.head())
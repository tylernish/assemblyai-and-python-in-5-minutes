## Tutorial: https://towardsdatascience.com/using-python-to-push-your-pandas-dataframe-to-google-sheets-de69422508f
#Keeping JSON key info in the same folder as this script

import pandas as pd
import gspread
import df2gspread as d2g
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'galvanic-botany-376415-1b464d71a294.json', scope)
gc = gspread.authorize(credentials)

spreadsheet_key = '1UTAUlwjTt0iJCtQQ3hxtDhIva-ELGcUJ41bIM8FFduk' 
## you get this^ from the url in a google sheet

wks_name = 'Master' ##Name of the work sheet you want to write on

d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)

## Tutorial: https://docs.gspread.org/en/latest/oauth2.html
## https://docs.gspread.org/en/latest/user-guide.html
# This file can read data from an Excel file
##TO do this you need to first share the excel 
# file with the 'client email' in the service account key data: 
# podcast-data@galvanic-botany-376415.iam.gserviceaccount.com

import gspread
import pandas as pd

##gc = gspread.service_account()
gc = gspread.service_account(filename='galvanic-botany-376415-1b464d71a294.json')

sh = gc.open("Podcast Data")

def getIndex(value, wrksName): ##find where a value is located, and which worksheet to search
    ##print(sh.sheet1.get('B1'))
    worksheet = sh.worksheet(wrksName)
    cell = worksheet.find(str(value))
    ##print("Found something at R%sC%s" % (cell.row, cell.col))
    if cell is None:
        return None
    else:
        return [cell.row, cell.col]
    
def getValue(cellIndex, wrksName):
    worksheet = sh.worksheet(wrksName)
    return worksheet.acell(cellIndex).value
    #cellIndex can be like 'B1' or 'A9'

#ex input: 4, Episode_Name, df ==> 'The Take'
def getDfValue(row, columnName, df):
    return df._get_value(row-2, columnName) 

### Functions to add later for ease of use

## returns true or false
## check if this episode has a transcript already
def episodeTranscriptExists(episodeName, wrksName):
    episodeRow = getIndex(episodeName, wrksName)[0] ##returns a list so need to access the row with [0]
    #print('****This should be the transcript of the episode ' +episodeName + ', if it exists: '+str(getValue('H'+str(episodeRow), wrksName)))
    return (pd.notna(getValue('H'+str(episodeRow), wrksName)))##return true or false, whether the value of H# (# being the row of the episodeName) (H being the transcript column) is None or is something

def isWrksEmpty(wrksName):
    worksheet = sh.worksheet(wrksName)
    return worksheet.acell('A2').value is None #if it is none then returns true

## def lookForShow(showName, wrksName)

## def lookForEpisode(episodeName, showName, wrksName)

## def getTranscript

## def getSummary


# cell = worksheet.find("Dough")

# print("Found something at R%sC%s" % (cell.row, cell.col))

def readDf(wrks_name):
    worksheet = sh.worksheet(wrks_name)

    data = worksheet.get_all_values()
    headers = data.pop(0)

    df = pd.DataFrame(data, columns=headers)
    s_replace = df.replace(['NaN', 'None', ''], float('nan'))
    print(s_replace)

    return s_replace

def nextOpenRow(wrksName):
    worksheet = sh.worksheet(wrksName)
    print('Here is the worksheet Row Count: '+str(worksheet.row_count))
    cols = worksheet.range(1, 1, worksheet.row_count, 10)#checks if values appear in the first 2 cols of each row
    row = max([cell.row for cell in cols if cell.value]) + 1
    print('The next open row is ' + str(row))
    return row

def main():
    nextOpenRow("SheetTest")

if __name__ == '__main__':
    #main2()
    main()
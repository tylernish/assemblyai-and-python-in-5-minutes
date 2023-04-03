#Sends data directly to a Google Sheet based on the credentials and the spreadsheet key
## Tutorial: https://towardsdatascience.com/using-python-to-push-your-pandas-dataframe-to-google-sheets-de69422508f
#Keeping JSON key info in the same folder as this script

import pandas as pd
import gspread
import df2gspread as d2g
from df2gspread import df2gspread as d2g
import gspread_dataframe as gd
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import time

import scrape_func
import read
import summarize_func
import search_func

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'galvanic-botany-376415-1b464d71a294.json', scope)
gc = gspread.authorize(credentials)

spreadsheet_key = '1UTAUlwjTt0iJCtQQ3hxtDhIva-ELGcUJ41bIM8FFduk' 
## you get this^ from the url in a google sheet

def write(wrks_name, input_df): #example write('Master', a_df, )
    if input_df.empty:
        print('Nothing to write, dataframe is empty')
    else:
        sh = gc.open("Podcast Data")
        worksheet = sh.worksheet(wrks_name)
        worksheet.clear()
        set_with_dataframe(worksheet=worksheet, dataframe=input_df, include_index=False,
        include_column_header=True, resize=True)
        ## This works! However, it also includes an extra column to the right that counts the number of episodes uploaded at once
        #d2g.upload(input_df, spreadsheet_key, wrks_name, credentials=credentials, row_names=True)
        print("*******Successfully uploaded the dataframe to worksheet: "+ wrks_name)

#Update a specific worksheet, and at a certain location like [2,8], update the value 
def updateCell(wrks_name, location, updateVal):
    sh = gc.open("Podcast Data")
    worksheet = sh.worksheet(wrks_name)
    #worksheet.update('B1', 'Bingo!')
    worksheet.update_cell(location[0], location[1], updateVal)
    #worksheet.update('A1:B2', [[1, 2], [3, 4]])

def updateSection(wrks_name, section, updateVals_df):
    sh = gc.open("Podcast Data")
    worksheet = sh.worksheet(wrks_name)
    dfListForm = updateVals_df.values.tolist()
    #print(dfListForm) #printing empty list sometimes $$
    worksheet.update(section, dfListForm)
    #worksheet.update('A1:B2', [[1, 2], [3, 4]])
    print('SUCCESSFULLY UPDATED SECTION THAT WAS MISSING INFO')

# ##Want to add df values if they don't already exist
# def addDf(wrks_name, df_to_add):
    # counter = 1
    # iterateDf = 0
    # goOn = True
    # while goOn:
    #     showName = read.getValue('B'+str(counter), wrks_name) 
    #     if showName == None: ##If the show doesn't exist (reached empty value row therefore the last row)
    #         print('**This show does not exist in the Google Sheet yet!')
    #         goOn = False
    #         updateSection(wrks_name, 'B'+str(counter)+':J'+str(counter - 1 + df_to_add.shape[0]), df_to_add)#df.shape[0] is the number of rows
    #     elif showName == df_to_add.iloc[iterateDf]["Show"]: ##if episodes of this show already exist
    #         #********for testing purposes we will leave this  out for now
    #         #if read.getValue('D'+str(counter), wrks_name) == df_to_add.iloc[iterateDf]["Episode"]: ##check if the same episode exists
    #         print('**This show exists in the Google Sheet already! Add code to append new episodes or summaries later') 
    #         addNewEpisodes(wrks_name, df_to_add)
    #         goOn = False   
    #     counter+=1


def addNewEpisodes(wrks_name, df_to_add):
    if df_to_add.empty:
        print('No new episodes to add!')
    else:
        sh = gc.open("Podcast Data")
        worksheet = sh.worksheet(wrks_name)
        # existing = gd.get_as_dataframe(worksheet)
        # updated = existing.append(df_to_add)
        # updated = updated.dropna(inplace = True)
        # gd.set_with_dataframe(worksheet, updated)

        #this worked but it put the values in the wrong columns
        df_values = df_to_add.values.tolist()
        sh.values_append(wrks_name, {'valueInputOption': 'RAW'}, {'values': df_values})
        #https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
    # else:
    #     #finnd what place I can put this
    #     dfBottom = str(read.nextOpenRow(wrks_name))
    #     newDfBottom = str(read.nextOpenRow(wrks_name) + len(df_to_add))
    #     newSection = 'B' + dfBottom + ':I' + newDfBottom ##B to I because Summary is not included yet
    #     updateSection(wrks_name, newSection, df_to_add)
    #     ##First attempt below, but I realized I already check if the episode exists already before I transcribe and create df, so df_to_add doesn't need to be checked:
    
    # # # for columnsName, columnData in df_to_add.iteritems():
    # # #     if 'Column Name'
    # # newEpisode_df = df_to_add.loc[read.getIndex(df_to_add.get('Episode'), wrks_name)==None]
    # # ##create a new dataframe using the old one where only rows with an episode that doesn't exist in read.getIndex (excel sheet)
    # # if newEpisode_df.empty:
    # #     print('No new episodes to add!')
    # # else:
    # #     newSection = 'B' + str(read.nextOpenRow(wrks_name)) + ':I' +  str(read.nextOpenRow(wrks_name) + len(newEpisode_df)) ##B to I because Summary is not included yet
    # #     updateSection(wrks_name, newSection, newEpisode_df)

def addSummaries(wrks_name, episodeName):
    #Now add in the summary of the transcript
    #location = [10, read.]
    #print("")
    episodeIndex = read.getIndex(str(episodeName), wrks_name)#need first element (row) out of that 2 length list for the index: [row,col]
    print("*****Episode Name's Index is: " + str(episodeIndex))
    if episodeName is None or pd.isna(episodeName):
        print("That episode either does not exist, or there was an issue with saving the episode data to the excel file")
        
    else:
        print("input for read.getValue("+ 'H' + str(episodeIndex[0])+", " + wrks_name+')')
        transcript = read.getValue('H' + str(episodeIndex[0]), wrks_name)
        #print(transcript)
        summaryIndex = [episodeIndex[0], episodeIndex[1]+6]
        #send the summaries to the google sheet
        print('Adding in the missing summary for the episode')
        updateCell(wrks_name, summaryIndex, summarize_func.summarizeTranscript(transcript))
        print('Cell updated with summary')

# ## Input
# ## Output
# ## Purpose: 
#     # check if any cells in a row are empty, 
#     # especially useful in the case of when Podcast Request 
#     # form creates an incomplete row with only the podcast 
#     # name and episode name
#     # If transcript isn't there but the name of the episode is
#     # scrape only the missing data and update that section 
#     # with missing data
# def sendMissingRowData(wrks_name, row):
#     print('SendMissingData being run!')
#     rowString = str(row)
#     seriesName = read.getValue('A'+rowString, wrks_name)
#     episodeNameCell = read.getValue('C'+rowString, wrks_name)

#     print('Checking if row '+ rowString + ' has episodeName != None and transcript == None ')
#     if (episodeNameCell != None and read.getValue('H'+rowString, wrks_name)==None):## and read.getValue('B'+rowString)==None):
#         print('turns out to be true! scraping the rest of the missing data and inserting it')
#         url = search_func.get_google_podcasts_link(seriesName)
#         updatedRow = scrape_func.download_missing_podcast_data(episodeNameCell, url, wrks_name)
#         sectionToUpdate = 'A'+rowString+':H'+rowString
#         updateSection(wrks_name, sectionToUpdate, updatedRow)
#         addSummaries(wrks_name, episodeNameCell)

## Input
## Output
## Purpose: 
    # check if any cells in a row are empty, 
    # especially useful in the case of when Podcast Request 
    # form creates an incomplete row with only the podcast 
    # name and episode name
    # If transcript isn't there but the name of the episode is
    # scrape only the missing data and update that section 
    # with missing data
    # ********* DF version, so it doesn't have so many API calls
def sendMissingRowData(wrks_name, df, row):
    print('SendMissingData being run! On DF row ' + str(row))
    row = row+2
    rowString = str(row)
    print('Changing this to be row '+rowString + ' for GS')
    #seriesName = read.getValue('A'+rowString, wrks_name)
    #episodeNameCell = read.getValue('C'+rowString, wrks_name)
    seriesName = read.getDfValue(row,'Podcast_Series', df)
    episodeNameCell = read.getDfValue(row, 'Episode_Name', df)
    episodeGoogleURLCell = str(read.getDfValue(row, 'Google URL', df))
    print('FOR TESTING*** Here is the cells episodeGoogleURLCell data: '+ episodeGoogleURLCell)

    print('Checking if GSpreadsheet row '+ rowString + ' has episodeName != None and transcript == None ')
    print('EpisodeName is: ' + str(episodeNameCell))
    #if (episodeNameCell != None and read.getValue('H'+rowString, wrks_name)==None):## and read.getValue('B'+rowString)==None):
    if (pd.notna(episodeNameCell)):
        print('EpisodeNameCell exists')
        # if there is no transcript, fill in all other missing data
        transcript = read.getDfValue(row, 'Transcript', df)
        if (pd.isna(transcript) or (transcript is None)):## and read.getValue('B'+rowString)==None):
           sendMissingDataFromEpisodeName(wrks_name, episodeNameCell, row, seriesName, rowString)

        # if there was a transcript, check if there is a summary
        elif (pd.isna(read.getDfValue(row, 'Summary', df))): #if not
            print('Only a summary was missing from the episode name input: '+episodeNameCell)
            addSummaries(wrks_name, episodeNameCell)#add one
    
    elif (pd.notna(episodeGoogleURLCell) and (episodeGoogleURLCell != 'nan')):
        print("********There is a URL form that was created from Webflow")
        # if there is no transcript, fill in all other missing data
        transcript = read.getDfValue(row, 'Transcript', df)
        if (pd.isna(transcript) or (transcript is None)):## and read.getValue('B'+rowString)==None):
           print('\tThere is also no transcript. Running sendMissingDataFromURL')
           sendMissingDataFromURL(wrks_name, episodeGoogleURLCell, df, row, rowString)

#Only gets called when there is an empty row with only a google podcasts URL attached 
def sendMissingDataFromURL(wrks_name, episodeGoogleURLCell, df, row, rowString):
    print('turns out to be true! No transcript but there is a Google Podcasts URL. \n***************Scraping the rest of the missing data and inserting it')
    url = episodeGoogleURLCell
    # $$ this below is returning an empty list or df
    updatedRow = scrape_func.download_missing_podcast_data_from_episode_URL(url, wrks_name) #this should only be of height 1 but it still might be in a list of lists or a df so might not act like a row, look for POSSIBLE ERRORS or BUGS
    if updatedRow.empty:
        print('Could not find the searched for episode, deleting this row so that later time is not wasted trying to find data again')
        sectionToUpdate = 'A'+rowString+':I'+rowString
        sh = gc.open("Podcast Data")
        worksheet = sh.worksheet(wrks_name)
        worksheet.delete_rows(row)#Will delete the row not being used
    else:
        print('\n\n******Here is the variable updated Row, this should not be empty:\n')
        print(updatedRow)
        sectionToUpdate = 'A'+rowString+':I'+rowString
        updateSection(wrks_name, sectionToUpdate, updatedRow)
        time.sleep(5) #Trying to wait a bit here because I think that the episode name is being searched for too soon, might need to move up
        episodeNameCell = read.getDfValue(row, 'Episode_Name', df)
        print("Episode name cell content is: "+str(episodeNameCell) +', for row: '+str(row))
        addSummaries(wrks_name, episodeNameCell)


def sendMissingDataFromEpisodeName(wrks_name, episodeNameCell, row, seriesName, rowString):
    print('turns out to be true! No transcript but there is a episode name. \n***************Scraping the rest of the missing data and inserting it')
    url = search_func.get_google_podcasts_link(seriesName)
    # $$ this below is returning an empty list or df
    updatedRow = scrape_func.download_missing_podcast_data(episodeNameCell, url, wrks_name) #this should only be of height 1 but it still might be in a list of lists or a df so might not act like a row, look for POSSIBLE ERRORS or BUGS
    if updatedRow.empty:
        print('Could not find the searched for episode, deleting this row so that later time is not wasted trying to find data again')
        sectionToUpdate = 'A'+rowString+':I'+rowString
        sh = gc.open("Podcast Data")
        worksheet = sh.worksheet(wrks_name)
        worksheet.delete_rows(row)#Will delete the row not being used
    else:
        print('\n\n******Here is the variable updated Row, this should not be empty:\n')
        print(updatedRow)
        sectionToUpdate = 'A'+rowString+':I'+rowString
        updateSection(wrks_name, sectionToUpdate, updatedRow)
        addSummaries(wrks_name, episodeNameCell)


## Input
## Output
## Purpose: 
    # run sendMissingRowData on each row, to check if data
    # is missing and add data if it is missing.
def updateSheetData(wrks_name):
    if read.isWrksEmpty(wrks_name):
        print('Google sheet is empty!')
    else:
        df = read.readDf(wrks_name)
        for x in range(0, read.nextOpenRowNumber(wrks_name)-2): #start at row 2 -2 because row 1 is just the column headers but df doesn't include headers and counts row 1 at 0
            print('Attempting to send missing row data for df row #'+str(x))
            sendMissingRowData(wrks_name, df, x)

def main2():
    podname = input("Please input the name of the podcast series you would like to download and send to an excel sheet: \n")
    # podname = str(podname)
    #url = scrape_func.find_podcast(podname)   #input("Please input the URL of the podcast series you would like to download and send to an excel sheet: \n")
    
    
    #url = input("Please input the URL of the podcast series you would like to download and send to an excel sheet: \n")
    
    url = search_func.get_google_podcasts_link(podname)

    #worksheet = input('Please enter the name of the worksheet: \n')
    worksheet = "Sheet9" #Hardcoded this in for now

    input_data = scrape_func.download_podcasts(url, worksheet)
    
    # Check if there is data there already
    # If not
    # write all the data from show name to transcript, to the google sheet
    if read.isWrksEmpty(worksheet):
        print('Google sheet is empty!')
        write(worksheet, input_data) 
    # If so, 
    #   for each row in the data frame check if that episode data already exists
    #       if so 
    #           print that this episode data already exists on this spreadsheet    
    #       if not, add data to new rows towards the bottom
    else:
        print('Google Sheet had info already!')
        #addDf(worksheet, input_data)
        addNewEpisodes(worksheet, input_data)
   
    episodeToSummarize = input("Please input the name of the episode you would like to summarize:\n")
    addSummaries(worksheet, episodeToSummarize)

def main():
    updateSheetData('Sheet9')
    #read.readDf('Sheet9')

if __name__ == '__main__':
    #main2()
    main()
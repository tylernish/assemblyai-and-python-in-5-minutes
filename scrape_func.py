## This script will download (maybe every) episodes of a podcast
## with the google podcasts URL you hardcode in
## I can change this to take in an input
## However I am not sure this is what we would want

import requests
from bs4 import BeautifulSoup
import wget # to download files
import pandas as pd
import os

import transcribe_func
import summarize_func
import read

import requests


def find_podcast(name):
    # Build the URL to the Google Podcasts API
    url = f"https://podcasts.google.com/search/{name}"

    try:
        # Make a GET request to the API
        response = requests.get(url)
        #print('Here is all the data gotten from that podcast search before parsed into JSON: \n'+str(response))

        # print("Here is response.results: " + response.results)

        # Parse the response as JSON
        data = response.json()
        #print(data)

        # Extract the podcast URL from the response
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            if result["podcastUrl"]:
                #print('***************\nHere is the podcastUrl being searched: \n'+result["podcastUrl"])
                return result["podcastUrl"]
    except ValueError:
        # Handle JSON decoding error
        pass

    return None

def download_podcasts(url, worksheet):
    ##Could get URL's and time range from an input
    timeInput = input('Enter the date for the podcast episode you want, like Jan 17, 2021 or Feb 2, 2020:\n') 
    #here asking for user input for a single podcast series url, changed so that url is already inputted
    ##url = input('Please enter the Google Podcasts URL for the Podcast Series you would like to summarize:\n')
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    title = soup.find('div', {'class':'ZfMIwb'}).text # This is the name of the show
    ## if folder exists already, don't create it
    if os.path.exists(title):
        print("The Podcast Series: '"+title+ ",' has been downloaded previously. Checking for updates.")
        # # d = {}
        # # df = pd.DataFrame(data=d)
        # df = pd.DataFrame()
        # return df
    else: ## if not then create the folder
        os.mkdir(title) # make a new folder to contain podcasts from the same show
    i = 0
    time_l = []
    ID_l = []
    description_l = []
    length_l = []
    link_l = []
    name_l = []
    transcript_1 = []
    summary_1 = ['None']
    for podcast in soup.find_all('a', {'role':'listitem'}):
        time = podcast.find('div', {'class':'OTz6ee'}).text
        #print(time)
        
        # if (time.startswith('Jan 30') or time.startswith('Feb 3')) and (time.endswith('2023')):
        if(time == timeInput):
            i += 1
            time_l.append(time)
            
            link = podcast.find('div', {'jsname':'fvi9Ef'})['jsdata'].split(';')[1]
            link_l.append(link)
            
            name = podcast.find('div', {'class':'e3ZUqe'}).text
            name_l.append(name)
            
            print(i, ":", time)
            
            fileID = time.replace(" ", "_").replace(",", "") # +'.mp3'##added this
            if (os.path.exists(title+'/'+fileID+'.mp3')):
                print('Episode is downloaded already')
            else:
                filename = wget.download(link, out=title)
                os.rename(filename, title+'/'+ fileID +'.mp3')#turns things like Jan 4, 2021 into Jan_4_2021
                #os.rename(filename, title+'/audio'+str(i)+'.mp3') # use if the downloaded name is always the same
                # ID_l.append('audio'+str(i))                         #^
                # ID_l.append(str(i)) # ID is just the filename for later access
            print('Does this episode exist in the Google Sheet already?')
            indexOfEpisode = read.getIndex(name, worksheet)
            if indexOfEpisode is None: #if the episode doesn't exist in the google sheet...
                print('**Episode data not in Google Sheet yet.')
                # time_l.append(time)
                # link_l.append(link)
                # name_l.append(name)
                ID_l.append(fileID) 
                
                try: # sometimes there's no description
                    description = podcast.find('div', {'class':'LrApYe'}).text
                except:
                    description = 'None'
                if description is None:
                    description = 'None'
                description_l.append(description)
                
                length = podcast.find('span', {'class':'gUJ0Wc'}).text
                length_l.append(length)

                transcription = transcribe_func.audioToText(title+'/'+fileID+'.mp3', True)##true means it is a local file
                transcript_1.append(transcription)

                # ***********Going to do the summary later **************referencing the transcript that is in the cells
                
                ##Call the summarize method
                # print('Summary method called on the transcription!')
                # summary = summarize_func.summarizeTranscript(transcription)

                # print('Appending this Transcript summary: ' + summary)
                
                # summary_1.append(summary)
            else:
                print("This episode data is already in the google sheet at: ")
                print(str(indexOfEpisode))
    
    df = pd.DataFrame(list(zip([title]*len(ID_l), ID_l, name_l, time_l, description_l, length_l, link_l, transcript_1, summary_1)), 
                    columns =['Podcast_Series', 'Item ID', 'Episode_Name', 'Time', 'Description', 'Length', 'Link', 'Transcript', 'Summary'])
    #print(df.to_string())
    ##Save the file as a csv and maybe you can then save the entire transcripts and summaries there as well
    ##df.to_csv(title+'\\'+ title + '_Details.csv',na_rep='Unkown') # missing value save as Unknown
    print('*****Successfully scraped the podcast audio and details')
    return df


def download_missing_podcast_data_from_episode_URL(url, worksheet):
    ##Could get URL's and time range from an input
  ##  timeInput = input('Enter the date for the podcast episode you want, like Jan 17, 2021 or Feb 2, 2020:\n') 
    #here asking for user input for a single podcast series url, changed so that url is already inputted
    ##url = input('Please enter the Google Podcasts URL for the Podcast Series you would like to summarize:\n')
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    episodeName = soup.find('div', {'class':'wv3SK'}).text
    title = (soup.find('div', {'class':'PRPYJc'}).text)[19:] #need to remove the 'More episodes from ' characters to just get the series name

    #Tried this (below) instead of including the entire function basically the same but it didn't work because the xml format of the page is different on the Episodes page and the Podcast series page
    #return download_missing_podcast_data(episodeName, url, worksheet)
    
    ## if folder exists already, don't create it
    if os.path.exists(title):
        print("The Podcast Series: '"+title+ ",' has been downloaded previously. Checking for updates.")
        # # d = {}
        # # df = pd.DataFrame(data=d)
        # df = pd.DataFrame()
        # return df
    else: ## if not then create the folder
        os.mkdir(title) # make a new folder to contain podcasts from the same show
    i = 0
    time_l = []
    ID_l = []
    description_l = []
    length_l = []
    link_l = []
    name_l = []
    transcript_1 = []
    summary_1 = ['None']
    
    # soup.find('div', {'class':'wv3SK'}).text
    time = soup.find('div', {'class':'Mji2k'}).text

    for podcast in soup.find_all('a', {'role':'listitem'}):
        # time = podcast.find('div', {'class':'OTz6ee'}).text
        # name = podcast.find('div', {'class':'e3ZUqe'}).text
        #print(time)
        
        # if (time.startswith('Jan 30') or time.startswith('Feb 3')) and (time.endswith('2023')):
        if(episodeName == episodeName):
            print("****Episodes with this name found!")
            i += 1 
            # time = podcast.find('div', {'class':'Mji2k'}).text

            time_l.append(time)

            link = soup.find('div', {'jsname':'fvi9Ef'})['jsdata'].split(';')[1]
            # link = podcast.find('div', {'jsname':'fvi9Ef'})['jsdata'].split(';')[1]
            link_l.append(link)
            
            name_l.append(episodeName)
            
            print(i, ":", time)
            
            fileID = time.replace(" ", "_").replace(",", "") # +'.mp3'##added this
            if (os.path.exists(title+'/'+fileID+'.mp3')):
                print('Episode is downloaded already')
            else:
                print('Starting download')
                filename = wget.download(link, out=title)
                os.rename(filename, title+'/'+ fileID +'.mp3')#turns things like Jan 4, 2021 into Jan_4_2021
                #os.rename(filename, title+'/audio'+str(i)+'.mp3') # use if the downloaded name is always the same
                # ID_l.append('audio'+str(i))                         #^
                # ID_l.append(str(i)) # ID is just the filename for later access
            print('Checking if the episode exists in the Google Sheet already')
            indexOfEpisode = read.getIndex(episodeName, worksheet)
            if indexOfEpisode is None: #if the episode doesn't exist in the google sheet...
                print('**Code thinks episode data not in Google Sheet yet. Only a URL must be there. \nThis should only ever be called when this episode name was just added to the google sheet')
            
            elif read.episodeTranscriptExists(episodeName, worksheet): #episode transcript doesn't exist
                    print("This episode data (or the transcript at least) is already in the google sheet at: ")
                    print(str(indexOfEpisode))
                    return pd.DataFrame() #IDK just return something random so this stops here
                    # time_l.append(time)
                    # link_l.append(link)
                    # name_l.append(name)
            # else:
            ID_l.append(fileID) 
            
            try: # sometimes there's no description
                description = soup.find('div', {'class':'QpaWg'}).text
            except:
                description = 'None'
            if description is None:
                description = 'None'
            description_l.append(description)
            
            length = (soup.find('span', {'class':'gUJ0Wc'}).text)[7:]
            # length = podcast.find('span', {'class':'gUJ0Wc'}).text
            length_l.append(length)

            transcription = transcribe_func.audioToText(title+'/'+fileID+'.mp3', True)##true means it is a local file
            transcript_1.append(transcription)

            # ***********Going to do the summary later **************referencing the transcript that is in the cells
            
            ##Call the summarize method
            # print('Summary method called on the transcription!')
            # summary = summarize_func.summarizeTranscript(transcription)

            # print('Appending this Transcript summary: ' + summary)
            
            # summary_1.append(summary)
        else:
            print("No episodes with this name found, no download started, dataframe returned empty")
    
    df = pd.DataFrame(list(zip([title]*len(ID_l), ID_l, name_l, time_l, description_l, length_l, link_l, transcript_1, summary_1)), 
                    columns =['Podcast_Series', 'Item ID', 'Episode_Name', 'Time', 'Description', 'Length', 'Link', 'Transcript', 'Summary'])
    #print(df.to_string())
    ##Save the file as a csv and maybe you can then save the entire transcripts and summaries there as well
    ##df.to_csv(title+'\\'+ title + '_Details.csv',na_rep='Unkown') # missing value save as Unknown
    print('*****Successfully scraped the podcast audio and details')
    return df


##Will only download and scrape data for podcast that has incomplete data
def download_missing_podcast_data(episodeNameInput, url, worksheet):
    ##Could get URL's and time range from an input
  ##  timeInput = input('Enter the date for the podcast episode you want, like Jan 17, 2021 or Feb 2, 2020:\n') 
    #here asking for user input for a single podcast series url, changed so that url is already inputted
    ##url = input('Please enter the Google Podcasts URL for the Podcast Series you would like to summarize:\n')
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    title = soup.find('div', {'class':'ZfMIwb'}).text # This is the name of the show
    ## if folder exists already, don't create it
    if os.path.exists(title):
        print("The Podcast Series: '"+title+ ",' has been downloaded previously. Checking for updates.")
        # # d = {}
        # # df = pd.DataFrame(data=d)
        # df = pd.DataFrame()
        # return df
    else: ## if not then create the folder
        os.mkdir(title) # make a new folder to contain podcasts from the same show
    i = 0
    time_l = []
    ID_l = []
    description_l = []
    length_l = []
    link_l = []
    name_l = []
    transcript_1 = []
    summary_1 = ['None']
    for podcast in soup.find_all('a', {'role':'listitem'}):
        # time = podcast.find('div', {'class':'OTz6ee'}).text
        name = podcast.find('div', {'class':'e3ZUqe'}).text
        #print(time)
        
        # if (time.startswith('Jan 30') or time.startswith('Feb 3')) and (time.endswith('2023')):
        if(name == episodeNameInput):
            print("****Episodes with this name found!")
            i += 1 
            time = podcast.find('div', {'class':'OTz6ee'}).text
            time_l.append(time)
            
            link = podcast.find('div', {'jsname':'fvi9Ef'})['jsdata'].split(';')[1]
            link_l.append(link)
            
            name_l.append(name)
            
            print(i, ":", time)
            
            fileID = time.replace(" ", "_").replace(",", "") # +'.mp3'##added this
            if (os.path.exists(title+'/'+fileID+'.mp3')):
                print('Episode is downloaded already')
            else:
                print('Starting download')
                filename = wget.download(link, out=title)
                os.rename(filename, title+'/'+ fileID +'.mp3')#turns things like Jan 4, 2021 into Jan_4_2021
                #os.rename(filename, title+'/audio'+str(i)+'.mp3') # use if the downloaded name is always the same
                # ID_l.append('audio'+str(i))                         #^
                # ID_l.append(str(i)) # ID is just the filename for later access
            print('Checking if the episode exists in the Google Sheet already')
            indexOfEpisode = read.getIndex(name, worksheet)
            if indexOfEpisode is None: #if the episode doesn't exist in the google sheet...
                print('**Code thinks episode data not in Google Sheet yet. Something is wrong. \nThis should only ever be called when this episode name was just added to the google sheet')
            else:
                if read.episodeTranscriptExists(name, worksheet): #episode transcript doesn't exist
                    print("This episode data (or the transcript at least) is already in the google sheet at: ")
                    print(str(indexOfEpisode))
                    # time_l.append(time)
                    # link_l.append(link)
                    # name_l.append(name)
                else:
                    ID_l.append(fileID) 
                    
                    try: # sometimes there's no description
                        description = podcast.find('div', {'class':'LrApYe'}).text
                    except:
                        description = 'None'
                    if description is None:
                        description = 'None'
                    description_l.append(description)
                    
                    length = podcast.find('span', {'class':'gUJ0Wc'}).text
                    length_l.append(length)

                    transcription = transcribe_func.audioToText(title+'/'+fileID+'.mp3', True)##true means it is a local file
                    transcript_1.append(transcription)

                    # ***********Going to do the summary later **************referencing the transcript that is in the cells
                    
                    ##Call the summarize method
                    # print('Summary method called on the transcription!')
                    # summary = summarize_func.summarizeTranscript(transcription)

                    # print('Appending this Transcript summary: ' + summary)
                    
                    # summary_1.append(summary)
        else:
            print("No episodes with this name found, no download started, dataframe returned empty")
    
    df = pd.DataFrame(list(zip([title]*len(ID_l), ID_l, name_l, time_l, description_l, length_l, link_l, transcript_1, summary_1)), 
                    columns =['Podcast_Series', 'Item ID', 'Episode_Name', 'Time', 'Description', 'Length', 'Link', 'Transcript', 'Summary'])
    #print(df.to_string())
    ##Save the file as a csv and maybe you can then save the entire transcripts and summaries there as well
    ##df.to_csv(title+'\\'+ title + '_Details.csv',na_rep='Unkown') # missing value save as Unknown
    print('*****Successfully scraped the podcast audio and details')
    return df
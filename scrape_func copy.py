##Copy of scrap_func.py on 2/10/23 when it worked but everything happened at once
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

def download_podcasts(url):
    ##Could get URL's and time range from an input
    #here asking for user input for a single podcast series url, changed so that url is already inputted
    ##url = input('Please enter the Google Podcasts URL for the Podcast Series you would like to summarize:\n')
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    title = soup.find('div', {'class':'ZfMIwb'}).text # This is the name of the show
    ## if folder exists already
    if os.path.exists(title):
        print("The Podcast Series: '"+title+ ",' has been downloaded previously. Checking for updates.")
        # d = {}
        # df = pd.DataFrame(data=d)
        df = pd.DataFrame()
        return df
    else:
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
            if (time.startswith('Feb') or time.startswith('Feb ')) and (time.endswith('2023')):
                i += 1
                time_l.append(time)
                
                link = podcast.find('div', {'jsname':'fvi9Ef'})['jsdata'].split(';')[1]
                link_l.append(link)
                
                name = podcast.find('div', {'class':'e3ZUqe'}).text
                name_l.append(name)
                
                print(i, ":", time)
                filename = wget.download(link, out=title)
                os.rename(filename, title+'/audio'+str(i)+'.mp3') # use if the downloaded name is always the same
                ID_l.append('audio'+str(i))                         #^

                ID_l.append(str(i)) # ID is just the filename for later access
                
                try: # sometimes there's no description
                    description = podcast.find('div', {'class':'LrApYe'}).text
                except:
                    description = 'None'
                if description is None:
                    description = 'None'
                description_l.append(description)
                
                length = podcast.find('span', {'class':'gUJ0Wc'}).text
                length_l.append(length)

                transcription = transcribe_func.audioToText( title+'/audio'+str(i) + ".mp3", True)##true means it is a local file
                transcript_1.append(transcription)

                # ***********Going to do the summary later **************referencing the transcript that is in the cells
                
                ##Call the summarize method
                # print('Summary method called on the transcription!')
                # summary = summarize_func.summarizeTranscript(transcription)

                # print('Appending this Transcript summary: ' + summary)
                
                # summary_1.append(summary)
        
        df = pd.DataFrame(list(zip([title]*len(ID_l), ID_l, name_l, time_l, description_l, length_l, link_l, transcript_1, summary_1)), 
                        columns =['Show', 'ID', 'Episode', 'Time', 'Description', 'Length', 'Link', 'Transcript', 'Summary'])
        #print(df.to_string())
        ##Save the file as a csv and maybe you can then save the entire transcripts and summaries there as well
        ##df.to_csv(title+'\\'+ title + '_Details.csv',na_rep='Unkown') # missing value save as Unknown
        print('*****Successfully scraped the podcast audio and details')
        return df

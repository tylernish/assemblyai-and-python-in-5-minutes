## This script will download (maybe every) episodes of a podcast
## with the google podcasts URL you hardcode in
## I can change this to take in an input
## However I am not sure this is what we would want

import requests
from bs4 import BeautifulSoup
import wget # to download files
import pandas as pd
import os

def download_podcasts(soup, title):
    i = 0
    time_l = []
    ID_l = []
    description_l = []
    length_l = []
    link_l = []
    name_l = []
    for podcast in soup.find_all('a', {'role':'listitem'}):
        time = podcast.find('div', {'class':'OTz6ee'}).text
        #print(time)
        if (time.startswith('Feb') or time.startswith('Jan')) and (time.endswith('2023')):
            i += 1
            time_l.append(time)
            
            link = podcast.find('div', {'jsname':'fvi9Ef'})['jsdata'].split(';')[1]
            link_l.append(link)
            
            name = podcast.find('div', {'class':'e3ZUqe'}).text
            name_l.append(name)
            
            #print(i, ":", time)
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
    
    df = pd.DataFrame(list(zip([title]*len(ID_l), ID_l, name_l, time_l, description_l, length_l, link_l)), 
                      columns =['Show', 'ID', 'Episode', 'Time', 'Description', 'Length', 'Link'])
    #print(df.to_string())
    ##Save the file as a csv and maybe you can then save the entire transcripts and summaries there as well
    df.to_csv(title+'\\'+ title + '_Details.csv',na_rep='Unkown') # missing value save as Unknown
    return df

##Could get URL's and time range from an input
#here asking for user input for a single podcast series url
url = input('Please enter the Google Podcasts URL for the Podcast Series you would like to summarize:\n')
URLs = [url]##['https://podcasts.google.com/feed/aHR0cHM6Ly9mZWVkcy5zaW1wbGVjYXN0LmNvbS9YQV84NTFrMw?sa=X&ved=0CAkQlvsGahcKEwjwqt2f9u3vAhUAAAAAHQAAAAAQAQ']


info_df_list = []
for url in URLs:
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    title = soup.find('div', {'class':'ZfMIwb'}).text # This is the name of the show
    if os.path.exists(title):
        #print("The Podcast Series: '"+title+ ",' is already downloaded.")
    else:
        os.mkdir(title) # make a new folder to contain podcasts from the same show
        df = download_podcasts(soup, title) # function details below
        info_df_list.append(df)
if info_df_list:##if a list is empty it is considered false, so if not empty then its true
    info_all_podcasts = pd.concat(info_df_list)##only concatenate if there is something to concatenate

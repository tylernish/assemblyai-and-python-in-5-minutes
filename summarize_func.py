## TO run:
## py summarize.py GatchyClip.mp4 --local --api_key=666bb857bdf84c0eba553e6fc101e62d
## that api key ^ is for AssemblyAI, but running this will summarize the transcription of a file

import os
import openai
import requests
##import transcribe_func #Will instead take an input for a transcription
import config
from nltk.probability import FreqDist #including because http://librarycarpentry.org/lc-tdm/08-counting-tokens/index.html#:~:text=To%20count%20tokens%2C%20one%20can,fdist%5B%22token%22%5D%20.

openai.api_key = config.OPENAI_API_KEY #"..."
#OPENAI_API_KEY='...'

#Takes in a text block transcript, and returns a summary
#Meant for smaller groups of text at a time
def summarizeText(text):
  print('\n\n***Piece of text to be summarized:\n'+text)
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Write a summary for this podcast conversation: " + text,  ## +"\n\nTl;dr",
    temperature=0.7,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1
  )
  #print response
  summary = response.choices[0].text #this should hopefully be text
  print('\n***A summary of the above piece of text: ' + summary)
  return summary

# Input: a compiled text of summaries
# Output: an overall summary based on the given text
def summarizeSummaries(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Using these summaries for parts of a podcast episode, write a general summary for the entire podcast episode: " + text,  ## +"\n\nTl;dr",
    temperature=0.7,
    max_tokens=300,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1
  )
  #print response
  summary = response.choices[0].text #this should hopefully be text
  print('\n**************King summary: ' + summary)
  return summary


# Input: an entire transcript to be summarized
# Output: a summary of that transcript
def summarizeTranscript(transcript):
  #See how many tokens are in the transcript
  fdist = FreqDist(transcript)
  tokenCount = fdist.N()  
  # fdist 
  ## print the fdist and you will see the occurences of each 
  ## token type, this could be useful later to perhaps eliminate 
  ## some tokens from the transcripts to shorten them

  if(tokenCount>5000):

    print("This transcript has " + str(tokenCount) + " tokens!! This is way too many!\nWe will attempt to split up the transcript into pieces to be summarized, and then summarize the summaries")
    
    ##Split the transcript on 'Speaker' as the delimiter, and add it back later
    d = "Speaker"
    speakerChangeList =  [d+e for e in transcript.split(d) if e] #s is a list of all the times a speaker changes
    
    ##response = 
    chunkSize = 0 # size of the chunk to summarize
    chunkToSummarize = '' # the text of the chunk to summarize
    summaries = '' # all of the summaries in on text variable
    speakerChangeListLength = len(speakerChangeList)
    i = 0
    while i < speakerChangeListLength:
    #for text in speakerChangeList:
      text = speakerChangeList[i]
      textSize = FreqDist(text).N() # tokens in the one piece of text
      if textSize > 5000:#if text is longer than 5000 don't increment counter, need to redo this same spot but with smaller text broken up
        print('One speaker speaks for more than 5000 tokens. This is an issue. Try to split this text up')
        speakerChangeList = speakerChangeList[0:i+1] + [text[0:int(len(text)/2)]] + [text[int(len(text)/2):-1]] + speakerChangeList[i+1:-1] ##Add in the list the two halves of that one long piece of text
        speakerChangeList.pop(i) #Remove from the list that one big chunk that was just split
        speakerChangeListLength= len(speakerChangeList)
      else:
        textTokenCount = textSize # tokens in the one piece of text
        chunkSize += textTokenCount # tokens in the current chunk
        ##WHAT if one piece of text is over the limit?, have to do this later ***************
        if chunkSize > 5000: # if adding that piece of text put it over the token limit
          chunkSize = textTokenCount #reset  chunk size to size of that piece of text
          summaries = summaries + '\nSummary of a part of the podcast:' + summarizeText(chunkToSummarize) #add the summary of the current chunk to the other summaries
        
          chunkToSummarize = text #reset current chunk to 
        else:
          chunkToSummarize = chunkToSummarize + text
        i = i+1
    summaries = summaries + '\nA summary of the last part of the podcast:' + summarizeText(chunkToSummarize)

    #finnally we can summarize the summaries
    #print('The giant block of summaries: \n' + summaries)
    print('***********Attempting to summarize the summaries!')
    kingSummary = summarizeSummaries(summaries)
    return kingSummary
  else:
    print('This transcript has less than 5000 tokens!')
    return summarizeText(transcript)


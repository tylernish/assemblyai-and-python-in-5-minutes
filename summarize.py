## TO run:
## py summarize.py GatchyClip.mp4 --local --api_key=666bb857bdf84c0eba553e6fc101e62d
## that api key ^ is for AssemblyAI, but running this will summarize the transcription of a file

import os
import openai
import requests
import transcribe
import config

openai.api_key = config.OPENAI_API_KEY #"..."
#OPENAI_API_KEY='...'


transcript = transcribe.main()

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Write a summary for this podcast conversation: " + transcript,  ## +"\n\nTl;dr",
  temperature=0.7,
  max_tokens=200,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=1
)

print(response)
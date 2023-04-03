## To Run Locally Without Storing (without storing and retrieving the API key successfully): 
##      py transcribe.py replace_with_name_of_audio_or_video_file --local --api_key=666bb857bdf84c0eba553e6fc101e62d
## This will only transcribe, not summarize

import argparse
import os
import utils
import config

# Output: Returns the transcription for an audio file
# Inputs: A string for the audio file name (probably 'audio#'), whether the file is local, and api key 
def audioToText(audioFileName, isLocal): 
    print("\t**audioToText being run - this operation costs money, make sure it runs ONCE per")
    #args.api_key = os.getenv("AAI_API_KEY")
    key = config.ASSEMBLYAI_API_KEY #Stored API key in config file
    if key is None:
        raise RuntimeError("AAI_API_KEY environment variable not set. Look back at function transcibe.py to see how it is done there.")

    # Create header with authorization along with content-type
    header = {
        'authorization': key,
        'content-type': 'application/json'
    }

    if isLocal:
        # Upload the audio file to AssemblyAI
        #print('\nRelative path of the audio file:'+audioFileName)
        upload_url = utils.upload_file(audioFileName, header)
    else:
        upload_url = {'upload_url': audioFileName}

    # Request a transcription
    transcript_response = utils.request_transcript(upload_url, header)
    ##print('************Transcript Response: \n'+str(transcript_response)) 
    #if there is an issue with a 'KeyError: 'id'' then the problem is with the current balance for using the AssemblyAI API

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utils.make_polling_endpoint(transcript_response)

    # Wait until the transcription is complete
    utils.wait_for_completion(polling_endpoint, header)

    # Request the paragraphs of the transcript
    #I  commented this out because it was causing an error and I don't know if it is ever used
    #paragraphs = utils.get_paragraphs(polling_endpoint, header)

    #5. #print transcription outputs
    ##print transcribed text response
    transcript_output_response = utils.get_transcript_output(polling_endpoint, header)

    transcript = ''#'----------\n'
    speakers = transcript_output_response['utterances']
    for speaker in speakers:
        result = (f'Speaker {speaker["speaker"]} \n {speaker["text"]} \n' )
        transcript+=result 
        ###print(result) ###prints each line one by one
    ###print(transcript) ###prints the entire transcript once finished

    #print('Successfully transcribed the audio.')
    return transcript

    # # Save and #print transcript
    # with open(args.audio_file +'.txt', 'w') as f:
    #     for para in paragraphs:
    #         #print(para['text'] + '\n')
    #         f.write(para['text'] + '\n')

    # return

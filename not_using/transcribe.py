## To Run Locally Without Storing (without storing and retrieving the API key successfully): 
##      py transcribe.py replace_with_name_of_audio_or_video_file --local --api_key=666bb857bdf84c0eba553e6fc101e62d
## This will only transcribe, not summarize

import argparse
import os
import utils
import config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audio_file', help='url to file or local audio filename')
    parser.add_argument('--local', action='store_true', help='must be set if audio_file is a local filename')
    parser.add_argument('--api_key', action='store', help='<YOUR-API-KEY>')

    args = parser.parse_args()

    ##added this if statement and 
    if args.audio_file is None:
        podName = input("Please enter the name of the Podcast Series:\n")
        podEpisode = input("Please enter the name of the Podcast Series:\n")
        args.audio_file = podName +"\\" + podEpisode ##needed two \'s cause one by itself would cause an error
        ## In theory this paragraph ^ should have been able to take in the podcast name 
        ## and episode so I can reference it from a folder I would have saved to this directory
        #print(podName+"\\"+podEpisode)
        if args.audio_file is None:
            raise RuntimeError("audio_file not set, glitching rn.")

    if args.api_key is None:
        #args.api_key = os.getenv("AAI_API_KEY")
        args.api_key = config.ASSEMBLYAI_API_KEY #Stored API key in config file
        if args.api_key is None:
            raise RuntimeError("AAI_API_KEY environment variable not set. Try setting it now, or passing in your "
                               "API key as a command line argument with `--api_key`.")

    # Create header with authorization along with content-type
    header = {
        'authorization': args.api_key,
        'content-type': 'application/json'
    }

    if args.local:
        # Upload the audio file to AssemblyAI
        #print(args.audio_file)
        upload_url = utils.upload_file(args.audio_file, header)
    else:
        upload_url = {'upload_url': args.audio_file}

    # Request a transcription
    transcript_response = utils.request_transcript(upload_url, header)

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utils.make_polling_endpoint(transcript_response)

    # Wait until the transcription is complete
    utils.wait_for_completion(polling_endpoint, header)

    # Request the paragraphs of the transcript
    paragraphs = utils.get_paragraphs(polling_endpoint, header)

    #5. #print transcription outputs
    ##print transcribed text response
    transcript_output_response = utils.get_transcript_output(polling_endpoint, header)

    transcript = '----------\n'
    speakers = transcript_output_response['utterances']
    for speaker in speakers:
        result = (f'Speaker {speaker["speaker"]} \n {speaker["text"]} \n' )
        transcript+=result 
        ###print(result) ###prints each line one by one
    ###print(transcript) ###prints the entire transcript once finished
    return transcript

    # # Save and #print transcript
    # with open(args.audio_file +'.txt', 'w') as f:
    #     for para in paragraphs:
    #         #print(para['text'] + '\n')
    #         f.write(para['text'] + '\n')

    # return

if __name__ == '__main__':
    main()
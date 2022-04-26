import argparse
import utils


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('audio_file', help='url to file or local audio filename')
    parser.add_argument('--local', action='store_true', help='must be set if audio_file is a local filename')
    parser.add_argument('--api_key', action='store',  help='<YOUR-API-KEY>')

    args = parser.parse_args()

    if args.api_key is None:
        with open("api_key.txt", "r") as f:
            lines = f.readlines()

        args.api_key = lines[0].strip()


    # Create header with authorization along with content-type
    header = {
        'authorization': args.api_key,
        'content-type': 'application/json'
    }

    if args.local:
        # Upload the audio file to AssemblyAI
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

    # Save and print transcript
    with open('transcript.txt', 'w') as f:
        for para in paragraphs:
            print(para['text'] + '\n')
            f.write(para['text'] + '\n')

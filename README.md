# How to run
Imports such as:
    'pip install lxml'
    'pip install nltk'
    all the other normal python imports

Then run 'monitor_func.py'

That's it.

Every 10 minutes it will check the google sheet named 'Podcast Data' for entries with no transcript or summararies and then fill the missing information in.

# speech-recognition-in-5-minutes-with-python

Repo for hosting tutorial code associated with the [AssemblyAI and Python in 5 Minutes](https://www.assemblyai.com/blog/assemblyai-and-python-in-5-minutes/) blog by [AssemblyAI](https://www.assemblyai.com/)


## Requirements

```console
$ pip install requests
```

## Usage:

If your AssemblyAI API key is stored as an environment variable called `AAI_API_KEY` file, then you can omit the optional `--api_key` argument.

```console
$ python transcribe.py audio_file [--local] [--api_key=<YOUR-API-KEY>"]
```

Example for hosted file:

```console
$ python transcribe.py https://github.com/AssemblyAI-Examples/assemblyai-and-python-in-5-minutes/raw/main/audio.mp3 --api_key=<YOUR-API-KEY>
```

Example for local file:

```console
$ python transcribe.py audio.mp3 --local --api_key=<YOUR-API-KEY>
```
My API Key:

666bb857bdf84c0eba553e6fc101e62d
import wave, math, contextlib, os, sys, json, subprocess
import numpy as np

from moviepy.editor import AudioFileClip
from vosk import Model, KaldiRecognizer

from pydub import AudioSegment
from pydub.silence import split_on_silence

def resample_ffmpeg(infile):
    stream = subprocess.Popen(
        ['ffmpeg', '-nostdin', '-loglevel', 'quiet', '-i',
        infile,
        '-ar', '16000','-ac', '1', '-f', 's16le', '-'],
        stdout=subprocess.PIPE)
    return stream

def recognize_stream(rec, stream):
    tot_samples = 0
    result = []
    while True:
        data = stream.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            tot_samples += len(data)
            result.append(json.loads(rec.Result()))
    result.append(json.loads(rec.FinalResult()))
    return result, tot_samples

def format_result(result, output_type='txt', words_per_line=7):
    final_result = ''
    if output_type == 'srt':
        subs = []
        for i, res in enumerate(result):
            if not 'result' in res:
                continue
            words = res['result']
            for j in range(0, len(words), words_per_line):
                line = words[j : j + words_per_line]
                s = srt.Subtitle(index=len(subs),
                        content = ' '.join([l['word'] for l in line]),
                        start=datetime.timedelta(seconds=line[0]['start']),
                        end=datetime.timedelta(seconds=line[-1]['end']))
                subs.append(s)
        final_result = srt.compose(subs)
    elif output_type == 'txt':
        for part in result:
            final_result += part['text'] + ' '
    return final_result

# a function that splits the audio file into chunks
# and applies speech recognition
def silence_based_conversion(path = ""):
    audio_file_name = "Audio/audio.wav"

    # create a directory to store the audio chunks.
    try:
        os.path.exists(audio_file_name)
    except(FileExistsError):
        # Extract audio clip
        audioclip = AudioFileClip(path)
        audioclip.write_audiofile(audio_file_name)

    # open the audio file stored in
    # the local system as a wav file.
    clip = AudioSegment.from_wav(audio_file_name)

    # split track where silence is 0.5 seconds
    # or more and get chunks
    chunks = split_on_silence(clip,
        min_silence_len = 500,
        silence_thresh = -40
    )

    # create a directory to store the audio chunks.
    try:
        os.mkdir('Audio/Chunks')
    except(FileExistsError):
        pass

    # move into the directory to
    # store the audio files.
    os.chdir('Audio/Chunks')

    i = 0

    # process each chunk
    for chunk in chunks:
        # Create 0.5 seconds silence chunk
        chunk_silent = AudioSegment.silent(duration = 10)

        # add 0.5 sec silence to beginning and
        # end of audio chunk. This is done so that
        # it doesn't seem abruptly sliced.
        audio_chunk = chunk_silent + chunk + chunk_silent

        # export audio chunk and save it in
        # the current directory.
        print("saving chunk{0}.wav".format(i))
        # specify the bitrate to be 192 k
        audio_chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav")

        # the name of the newly created chunk
        filename = 'chunk'+str(i)+'.wav'

        print("Processing chunk "+str(i))

        # get the name of the newly created chunk
        # in the AUDIO_FILE variable for later use.
        file = filename

        # Load model
        #model_path = "../../Models/vosk-model-en-us-0.22-lgraph/"
        model_path = "../../Models/vosk-model-small-en-us-0.15/"
        model = Model(model_path)

        # Set up recognizer
        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)

        result, tot_samples = recognize_stream(rec, resample_ffmpeg(file))
        final_result = format_result(result)
        print(final_result)

        f = open("../../Transcripts/test.txt", "a")
        f.write(final_result)
        f.write("\n")
        f.close()

        i += 1

    os.chdir('..')


if __name__ == '__main__':

    #print('Enter the audio file path')
    #path = input()

    silence_based_conversion("Videos/TestVideo.mp4")


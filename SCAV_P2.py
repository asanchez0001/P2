import os
import json


def getInfo(path='/Users/alvaro/BBB_1080p_60fps.mp4'):
    """
    Create a python script able to parse the ‘ffmpeg –i BBB.mp4’ file,
    which can mark at least 3 relevant data from the container
    """

    try:
        os.remove('metadata.json')
    except FileNotFoundError:
        print('metadata.json not found.')

    os.system('ffprobe -hide_banner -v quiet -show_format -show_streams '
              '-print_format json {0} > metadata.json'.format(path))

    f = open('metadata.json', 'r')
    data = json.load(f)
    duration = data['format']['duration']
    video_info = data['streams'][0]
    audio_info = data['streams'][1]
    f.close()

    dimensions = str(video_info['width']) + 'x' + str(video_info['height'])
    codecs = video_info['codec_name'], audio_info['codec_name']

    print('Dimensions: {0}'
          '\nCodecs: {1}'
          '\nDuration: {2} sec'.format(dimensions, codecs, duration))

    return dimensions, codecs, duration


def extractAudio(path='/Users/alvaro/BBB_1080p_60fps.mp4'):
    """
    You’re going to create a script in order to create a new BBB container:
    · Cut BBB into 1-minute only video.
    · Export BBB(1min) audio as MP3 stereo track.
    · Export BBB(1min) audio in AAC w/ lower bitrate
    Now package everything in a .mp4 with FFMPEG!!
    """

    try:
        os.remove('BBB_1minute.mp4')
        os.remove('BBB_mp3.mp4')
        os.remove('BBB_low_bitrate.mp4')
    except FileNotFoundError:
        print('BBB_1minute.mp4 not found.')

    # Shorten BBB video
    os.system('ffmpeg -i {0} -ss 00:05:20 -t 00:01:00 -c:v copy -c:a copy BBB_1minute.mp4'.format(path))

    # Merge only video and audio into two new BBB videos to see difference
    os.system('ffmpeg -i {0} -vcodec copy -acodec mp3 BBB_mp3.mp4'.format('BBB_1minute.mp4'))
    os.system('ffmpeg -i {0} -b:a 48k -vcodec copy BBB_low_bitrate.mp4'.format('BBB_1minute.mp4'))


def changeResolution(path='BBB_1minute.mp4', width=1920, height=1080):
    """
    Create a python script able to resize (resolution change) of any input given
    """

    try:
        os.remove('BBB_1minute_resized.mp4')
    except FileNotFoundError:
        print('BBB_1minute_resized.mp4 not found.')

    os.system('ffmpeg -i {0} -vf scale={1}:{2},setsar=1 -preset slow '
              '-crf 22 BBB_1minute_resized.mp4'.format(path, width, height))


def checkAudio(path='/Users/alvaro/BBB_1080p_60fps.mp4'):
    """
    Create a python script which will check the audio tracks of the video.
    Then, with this information, it will explain in which broadcasting standard
    the video can fit. I.e.: one AC-3 audio, that means it can be ATSC.
    """

    dimensions, codecs, duration = getInfo(path)

    print('\nBroadcasting Standards: ')
    if codecs[1].upper() == 'AAC':
        print('DVB', 'ISDB', 'DTMB')
    elif codecs[1].upper() == 'AC-3':
        print('DVB', 'ATSC', 'DTMB')
    elif codecs[1].upper() == 'MP3':
        print('DVB', 'DTMB')
    elif codecs[1].upper() == 'MP2':
        print('DTMB')
    elif codecs[1].upper() == 'DRA':
        print('DTMB')


if __name__ == '__main__':
    path_to_file = '/Users/alvaro/BBB_1080p_60fps.mp4'

    print('1. Relevant information (Dimensions, Codecs, Duration)\n'
          '2. BBB with MP3 / AAC audio stream\n'
          '3. Resize video\n'
          '4. Broadcasting Standards')

    input_option = int(input('Choose option: '))

    if input_option == 1:
        dim, cod, dur = getInfo(path=path_to_file)
    elif input_option == 2:
        extractAudio(path=path_to_file)
    elif input_option == 3:
        print('Output can be distorted if ratio not preserved!')
        input_width = int(input('Width: '))
        input_height = int(input('Height: '))
        changeResolution(width=input_width, height=input_height)
    elif input_option == 4:
        checkAudio(path=path_to_file)

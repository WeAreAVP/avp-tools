'''
Purpose: Converts TXT files to WebVTT files.

Usage: 'python [path to otter-txt-to-vtt.py]' or 'python3 [path to otter-txt-to-vtt.py]' depending on your enviroment config.
'''

import os
import re
from datetime import datetime
from datetime import timedelta

use = input('Would you like to convert a single TXT or all the TXTs in a folder? Type "file" or "folder": ').strip().lower()

while use != 'file' and use != 'folder':
    print('Looks like you didn\'t type "file" or "folder". Please try running the script again')
    use = input('Would you like to convert a single TXT or all the TXTs in a folder? Type "file" or "folder": ').strip().lower()

print()

if use == 'file':
    input_path = input('What is the full path of the TXT file?: ').strip()
elif use == 'folder':
    input_path = input('What is the full path of the folder containing the TXT?: ').strip()

if os.name == 'posix':
    input_path = input_path.replace('\\','')
else:
    input_path = input_path.replace('\\','/')

path = input_path.strip().strip('"')

if use == 'file':
    file = '/'.join(path.split('/')[-1:])
    path = '/'.join(path.split('/')[:-1])

output_folder = path + '/vtts'

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
except:
    print()
    print('Sorry,', path, 'is not a valid directory.')
    print()
    exit()

def process_file(file):
    f = open(output_folder + '/' + file[:-4] + '.vtt', 'w')

    first_line = True

    with open(path + '/' + file, 'r') as txt:
        saved_speaker = None
        speaker_bool = False

        storage = ''
        start_time = None
        end_time = None
        new_start_time = None

        for line in txt:
            if line.strip() == 'Transcribed by https://otter.ai':
                continue

            if first_line:
                f.write('WEBVTT' + '\n')
                f.write('\n')
                first_line = False

            times = re.findall(r'\d{1,2}:\d{2}', line)

            if times:
                start_time = new_start_time
                time = times[0]

                time_len = len(time)

                speaker = line.strip()[:-time_len].strip()
                speaker_bool = False

                split_time = time.split(':')

                if len(split_time) == 1:
                    time = '00:00:' + time
                elif len(split_time) == 2:
                    if len(split_time[0]) == 0:
                        time = '00:00' + time
                    elif len(split_time[0]) == 1:
                        time = '00:0' + time
                    elif len(split_time[0]) == 2:
                        time = '00:' + time
                    else:
                        print('The time format is strange. Please contact AVP.')
                        exit()
                elif len(split_time) == 3:
                    if len(split_time[0]) == 0:
                        time = '00' + time
                    elif len(split_time[0]) == 1:
                        time = '0' + time
                    elif len(split_time[0]) > 2:
                        print('The time format is strange. Please contact AVP.')
                        exit()
                elif len(split_time) > 3:
                    print('The time format is strange. Please contact AVP.')
                    exit()

                new_start_time = time + '.000'

                if start_time :
                    end_time = datetime.time(datetime.strptime(new_start_time, '%H:%M:%S.%f') - timedelta(milliseconds=1))
                    f.write(str(start_time) + ' --> ' + str(end_time)[:-3] + '\n')
                    f.write(storage)

                    storage = ''

                if speaker:
                    saved_speaker = speaker.upper()
                    speaker_bool = True
            else:
                if speaker_bool:
                    line = saved_speaker + ': ' + line
                    speaker_bool = False

                storage = storage + line
        
        end_time = datetime.time(datetime.strptime(new_start_time, '%H:%M:%S.%f') + timedelta(milliseconds=2000))
        f.write(str(new_start_time) + ' --> ' + str(end_time) + '.000\n')
        f.write(storage)

    f.close()

if use == 'file':
    if file[-4:] != '.txt':
        print('Sorry, file is not a .txt')
        exit()
    
    process_file(file)
elif use == 'folder':
    for file in os.listdir(path):
        if file[-4:] != '.txt':
            continue

        if file == '.DS_Store':
            continue

        if os.path.isdir(path + '/' + file):
            continue

        process_file(file)

print()
print('Finished converting TXTs to VTTs.')
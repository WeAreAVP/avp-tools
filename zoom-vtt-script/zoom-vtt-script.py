'''
Purpose: Converts Zoom .txt chat files to WebVTT files. Adjusts chat timestamps to transcript timestamps by subtracting the time the meeting started.

Usage: 'python [path to find-and-replace.py]' or 'python3 [path to find-and-replace.py]' depending on your enviroment config.
'''

import os
import re
from datetime import datetime
from datetime import timedelta

import demoji

demoji.download_codes()

def to_delta(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M:%S.%f').time()
    time_delta = timedelta(
        hours=time_obj.hour,
        minutes=time_obj.minute,
        seconds=time_obj.second,
        microseconds=time_obj.microsecond
    )

    return time_delta

use = input('Would you like to convert a single Zoom chat file or all the Zoom chat files in a folder? Type "file" or "folder": ').strip().lower()

while use != 'file' and use != 'folder':
    print('Looks like you didn\'t type "file" or "folder". Please try running the script again')
    use = input('Would you like to convert a single Zoom chat file or all the Zoom chat files in a folder? Type "file" or "folder": ').strip().lower()

if use == 'file':
    input_path = input('What is the full path of the Zoom .txt chat file?: ').strip().replace('\\','')
elif use == 'folder':
    input_path = input('What is the full path of the folder containing the Zoom .txt chat files? (Warning: This will attempt to convert all .txt files in this folder. Original files will be unaffected.): ').strip().replace('\\','')

if os.name == 'posix':
    input_path = input_path.replace('\\','')

path = input_path.strip().strip('"')

if use == 'file':
    file = '/'.join(path.split('/')[-1:])
    path = '/'.join(path.split('/')[:-1])

output_folder = path + '/converted_chats'

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
except:
    print()
    print('Sorry,', path, 'is not a valid directory.')
    print()
    exit()

offset_time = None

while not offset_time:
    offset_time_input = input("Please input the time that the Zoom call started as hours:minutes:seconds in military/24hr time (e.g. 16:32:40). ")
    offset_time = re.match(r'\d{2}:\d{2}:\d{2}', offset_time_input)

offset_time_group = offset_time.group()

offset_time_delta = to_delta(offset_time_group + '.000')

def process_file(file):
    with open(output_folder + '/' + file[:-4] + '.vtt', 'w') as vtt:
        vtt.write('WEBVTT' + '\n')

        with open(path + '/' + file, 'r') as chat:
            for line in chat:
                demojied_line = demoji.replace_w_desc(line)

                split_line = demojied_line.split('\t')

                if len(split_line) > 2:
                    print('Woah!')
                
                time = re.findall(r'\d{2}:\d{2}:\d{2}', split_line[0])
            
                if time:
                    if len(time) > 1:
                        print('There\'s an issue with the Zoom transcript timestamps')
                    else:
                        start_time_delta = to_delta(time[0] + '.000')
                        updated_start_delta = start_time_delta - offset_time_delta
                        str_start_delta = str(updated_start_delta)

                        if len(str_start_delta.split(':')[0]) < 2:
                            str_start_delta = '0' + str_start_delta
                        
                        end_time_delta = to_delta(time[0] + '.001')
                        updated_end_delta = end_time_delta - offset_time_delta
                        str_end_delta = str(updated_end_delta)

                        if len(str_end_delta.split(':')[0]) < 2:
                            str_end_delta = '0' + str_end_delta

                        vtt.write('\n' + str_start_delta + '.000 --> ' + str_end_delta[:-3] + '\n')

                        vtt.write(''.join(split_line[1:]))
                else:
                    vtt.write(''.join(split_line))

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
print('Finished converting Zoom chats to VTTs.')
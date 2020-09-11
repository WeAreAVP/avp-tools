'''
Purpose: 

Usage: 
'''

import os
import re
from datetime import datetime
from datetime import timedelta

use = input('Would you like to convert a single SRT or all the SRTs in a folder? Type "file" or "folder": ').strip().lower()

while use != 'file' and use != 'folder':
    print('Looks like you didn\'t type "file" or "folder". Please try running the script again')
    use = input('Would you like to convert a single SRT or all the SRTs in a folder? Type "file" or "folder": ').strip().lower()

if use == 'file':
    input_path = input('What is the full path of the SRT file?: ').strip().replace('\\','')
elif use == 'folder':
    input_path = input('What is the full path of the folder containing the SRTs?: ').strip().replace('\\','')

if os.name == 'posix':
    input_path = input_path.replace('\\','')

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

    with open(path + '/' + file, 'r') as srt:
        for line in srt:
            if first_line:
                f.write('WEBVTT' + '\n')
                f.write('\n')
                first_line = False
            
            times = re.findall(r'\d{2}:\d{2}:\d{2},\d{3}', line)

            if times:
                start_time = times[0].replace(',','.')

                end_time = times[1].replace(',','.')

                line = start_time + ' --> ' + end_time + '\n'

            f.write(line)

    f.close()


if use == 'file':
    if file[-4:] != '.srt':
        print('Sorry, file is not a .srt')
        exit()
    
    process_file(file)
elif use == 'folder':
    for file in os.listdir(path):
        if file[-4:] != '.srt':
            continue

        if file == '.DS_Store':
            continue

        if os.path.isdir(path + '/' + file):
            continue

        process_file(file)

print()
print('Finished converting SRTs to VTTs.')
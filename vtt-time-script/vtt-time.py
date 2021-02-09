'''
Purpose: Adjusts the timestamps of VTT files by setting the first transcript point to 00:00:00 and adjusting all other transcript points accordingly. Additionally, it can add a specified offset in case the first transcript point doesn't come at 00:00:00; for example, if the first speech comes at 00:00:13.

Usage: 'python [path to find-and-replace.py]' or 'python3 [path to find-and-replace.py]' depending on your enviroment config.
'''

import os
import re
from datetime import datetime
from datetime import timedelta

use = input('Would you like to adjust the timestamps of a single VTT or all the VTTs in a folder? Type "file" or "folder": ').strip().lower()

while use != 'file' and use != 'folder':
    print('Looks like you didn\'t type "file" or "folder". Please try running the script again')
    use = input('Would you like to adjust the timestamps of a single VTT or all the VTTs in a folder? Type "file" or "folder": ').strip().lower()

print()

if use == 'file':
    input_path = input('What is the full path of the VTT file?: ').strip()
elif use == 'folder':
    input_path = input('What is the full path of the folder containing the VTTs?: ').strip()

if os.name == 'posix':
    input_path = input_path.replace('\\','')
else:
    input_path = input_path.replace('\\','/')

path = input_path.strip().strip('"')

if use == 'file':
    file = '/'.join(path.split('/')[-1:])
    path = '/'.join(path.split('/')[:-1])

output_folder = path + '/fixed_vtts'

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
except:
    print()
    print('Sorry,', path, 'is not a valid directory.')
    print()
    exit()

check_manual_offset = input("Should there be any additional offset (yes/no)? ").lower().strip()

if check_manual_offset == 'yes' or check_manual_offset == 'y':
    manual_offset = input("In the format of hours:minutes:seconds.milliseconds (e.g. 00:00:00.000), when should the first timestamp occur? ")

def to_delta(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M:%S.%f').time()
    time_delta = timedelta(
        hours=time_obj.hour,
        minutes=time_obj.minute,
        seconds=time_obj.second,
        microseconds=time_obj.microsecond
    )

    return time_delta

def subtract_offset(time_delta, offset_delta):
    adjusted_delta = time_delta  + manual_offset_delta - offset_delta
    adjusted_time = str(adjusted_delta)

    split_adj_time = adjusted_time.split(':')

    if len(split_adj_time[0]) < 2:
        split_adj_time[0] = '0' + split_adj_time[0]
    
    decimal_split = split_adj_time[2].split('.')

    if len(decimal_split) < 2:
        split_adj_time[2] = decimal_split[0] + '.000'
    else:
        decimal_split[1] = decimal_split[1][:3]
        split_adj_time[2] = '.'.join(decimal_split)
    
    joined_time = ':'.join(split_adj_time)

    return joined_time

def process_file(file):
    f = open(output_folder + '/fixed_' + file, 'w')

    offset_time = ''
    offset_delta = ''

    with open(path + '/' + file, 'r') as vtt:
        for line in vtt:
            times = re.findall(r'\d{2}:\d{2}:\d{2}.\d{3}', line)

            if times:
                if not offset_time:
                    offset_time = times[0]
                    offset_delta = to_delta(offset_time)

                start_time = to_delta(times[0])

                adjusted_start = subtract_offset(start_time, offset_delta)

                end_time = to_delta(times[1])

                adjusted_end = subtract_offset(end_time, offset_delta)

                line = adjusted_start + ' --> ' + adjusted_end + '\n'

            f.write(line)

    f.close()

if check_manual_offset == 'yes' or check_manual_offset == 'y':
    try:
        manual_offset_delta = to_delta(manual_offset)
    except:
        print('The time offset was not correctly formatted.')
else:
    manual_offset_delta = to_delta('00:00:00.000')

if use == 'file':
    if file[-4:] != '.vtt':
        print('Sorry, file is not a .vtt')
        exit()

    process_file(file)
elif use == 'folder':
    for file in os.listdir(path):
        if file[-4:] != '.vtt':
            continue

        if file == '.DS_Store':
            continue

        if os.path.isdir(path + '/' + file):
            continue

        process_file(file)

print()
print('Finished correcting WebVTT timestamps.')
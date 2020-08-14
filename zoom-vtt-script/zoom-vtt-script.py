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

file = input("What is the path of the Zoom chat file?: ")

if os.name == 'posix':
    file = file.replace('\\','')

path = file.strip().strip('"')

output_path = path[:-4] + '.vtt'

offset_time = None

while not offset_time:
    offset_time_input = input("Please input the time that the Zoom call started as hours:minutes:seconds in military/24hr time (e.g. 16:32:40). ")
    offset_time = re.match(r'\d{2}:\d{2}:\d{2}', offset_time_input)

offset_time_group = offset_time.group()

offset_time_delta = to_delta(offset_time_group + '.000')

with open(output_path, 'w') as vtt:
    vtt.write('WEBVTT' + '\n')

    with open(path, 'r') as chat:
        for line in chat:
            demojied_line = demoji.replace_w_desc(line)

            split_line = demojied_line.split('\t ')

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

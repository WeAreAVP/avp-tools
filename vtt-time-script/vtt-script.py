import os
import re
from datetime import datetime
from datetime import timedelta

folder = input("What is the path of the folder where the VTTs are located? ")

if os.name == 'posix':
    folder = folder.replace('\\','')

path = folder.strip().strip('"')

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

if check_manual_offset == 'yes' or check_manual_offset == 'y':
    try:
        manual_offset_delta = to_delta(manual_offset)
    except:
        print('The time offset was not correctly formatted.')
else:
    manual_offset_delta = to_delta('00:00:00.000')

for file in os.listdir(path):
    if file == '.DS_Store':
        continue

    if os.path.isdir(path + '/' + file):
        continue

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

print()
print('Finished correcting WebVTT timestamps.')
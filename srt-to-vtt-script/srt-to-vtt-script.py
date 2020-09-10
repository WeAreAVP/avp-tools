import os
import re
from datetime import datetime
from datetime import timedelta

folder = input("What is the path of the folder where the SRTs are located? ")

if os.name == 'posix':
    folder = folder.replace('\\','')

path = folder.strip().strip('"')

output_folder = path + '/vtts'

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
except:
    print()
    print('Sorry,', path, 'is not a valid directory.')
    print()
    exit()

for file in os.listdir(path):
    if file[-4:] != '.srt':
        continue

    if file == '.DS_Store':
        continue

    if os.path.isdir(path + '/' + file):
        continue

    f = open(output_folder + '/' + file[:-4] + '.vtt', 'w')

    offset_time = ''
    offset_delta = ''

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

print()
print('Finished converting SRTs to VTTs.')
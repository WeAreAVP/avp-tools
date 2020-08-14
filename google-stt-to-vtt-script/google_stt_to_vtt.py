"""Google Speech-to-text to VTT -- 2020-05-22
This script converts a folder of Google JSON files to VTT (.vtt) format. Run on 
command line with the following parameters:
- absolute folder path
- (optional) format type ('transcript' for Google's default segmentation or 'fixed_length' for fixed duration--defaults to 'transcript')
- (optional) segment duration (if using 'fixed_length', integer in seconds for desired segment length
example: 'python3 google_stt_to_vtt.py fixed_length 30 "/path/to/my/files/" //breaks out transcript into 30 second segments
example: 'python3 google-stt_to_vtt.py "/path/to/my/files/" //default segments using Google's segmentation
All VTT files are output to a new /vtt directory inside the target folder."""
import json
from datetime import timedelta
from decimal import Decimal
import sys
import os

def format_time(t):
    td = str(timedelta(seconds=float(t)))
    #trim milliseconds
    mssplit = td.split('.')
    if len(mssplit) == 2:
        strtd = td[:-3]
    #zero fill ms
    else:
        strtd = mssplit[0] + '.000'
        #zero fill hour
    hsplit = strtd.split(':')
    if len(hsplit[0]) == 1:
        strtd = '0' + strtd
    return strtd

def splitIntoParts(data, part_type='transcript', part_dur=60):
  segments = data['response']['results']
  parts = []
  #this uses google's default segmentation
  if part_type == 'transcript':
    for s in segments:
        for a in s['alternatives']:
          part = {}
          part['words'] = a['transcript']
          part['start'] = float(a['words'][0]['startTime'].replace('s', ''))
          part['end'] = float(a['words'][0]['endTime'].replace('s', ''))
          parts.append(part)
  #this creates segments of duration specified in part_dur (default 1 minute)
  if part_type == 'fixed_length':
    #put all the words and their times into a single list
    all_words = []
    for s in segments:    
      for a in s['alternatives']:
        for w in a['words']:
          all_words.append(w)
      #convert time strings to seconds
    for a in all_words:
      a['startTime'] = float(a['startTime'].replace('s', ''))
      a['endTime'] = float(a['endTime'].replace('s', ''))
    #initialize variables for iterating through words and segmenting by fixed length
    interval = Decimal(part_dur)
    timerange = [0,interval]
    vtt_trans = []
    for w in all_words:
      #add words to a part until the start time exceeds the duration interval
      if Decimal(w['startTime']) >= timerange[0] and Decimal(w['startTime']) < timerange[1]:
          vtt_trans.append(w['word'])
      else:
        #once words exceed the part interval, add the part to the list of parts and start a new one
          part = {}
          part['start'] = timerange[0]
          part['end'] = timerange[1]
          part['words'] = ' '.join(vtt_trans)
          parts.append(part)
          timerange = [x + interval for x in timerange]
          vtt_trans = []
          vtt_trans.append(w['word'])
    #add last words
    part = {}
    part['start'] = timerange[0]
    part['end'] = timerange[1]
    part['words'] = ' '.join(vtt_trans)
    parts.append(part)
  return parts

def exportVTT(parts, filename):
  with open(filename, 'w') as v:
    v.write("WEBVTT\n\n")
    for p in parts:
        timeline = format_time(p['start']) + ' --> ' + format_time(p['end']) + '\n'
        speakerline = p['words'] + '\n\n'
        v.write(timeline)
        v.write(speakerline)

if __name__ == "__main__":

  #get CLI arguments
  inputfolder = sys.argv[1]
  if len(sys.argv) > 2:
    part_type = sys.argv[2]
  else:
    part_type = 'transcript'
  if len(sys.argv) > 3:
    part_dur = sys.argv[3]
  else:
    part_dur = 60

for f in os.listdir(inputfolder):
  if f[-4:] == 'json':
    inputfile = (inputfolder + '/' + f).replace('//', '/')
    with open(inputfile, 'r') as f:
        data = json.load(f)

    #split data into parts
    vtt = splitIntoParts(data, part_type=part_type, part_dur=part_dur)

    #export VTT
    #output into a vtt folder
    filepath = os.path.abspath(inputfile)
    vttpath = filepath + '/vtt'
    # if not os.path.exists(vttpath):
    #     os.makedirs(vttpath)
    if not os.path.exists('vtt'):
      os.makedirs('vtt')
    filestem = os.path.splitext(os.path.basename(inputfile
      ))[0]
    # outputfile = '/'.join([vttpath, filestem]) + '.vtt'
    outputfile = '/'.join(['vtt', filestem]) + '.vtt'
    exportVTT(vtt, outputfile)
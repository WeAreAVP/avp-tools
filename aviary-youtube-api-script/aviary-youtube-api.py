import requests
import json
import csv
import sys
import pytz
import datetime

utc = pytz.utc

def get_channel_page(channel_id, page_token=False):
    part = 'contentDetails'
    if page_token:
        r = requests.get('https://www.googleapis.com/youtube/v3/channels', params={'part':part,'maxResults':max_results,'id':channel_id,'key':api_key,'pageToken':page_token})
    else:
        r = requests.get('https://www.googleapis.com/youtube/v3/channels', params={'part':part,'maxResults':max_results,'id':channel_id,'key':api_key})

    response = r.json()

    for item in response['items']:
        try:
            playlist_id = item['contentDetails']['relatedPlaylists']['uploads']
            break
        except:
            continue

    print('\n')
    get_playlist_page(playlist_id)

def get_playlist_page(playlist_id, page_token=False):
    part = 'contentDetails'
    if page_token:
        r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={'part':part,'maxResults':max_results,'playlistId':playlist_id,'key':api_key, 'pageToken':page_token})
    else:
        r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={'part':part,'maxResults':max_results,'playlistId':playlist_id,'key':api_key})

    response = r.json()

    get_video_id(response, playlist_id)

def get_video_id(page_list, playlist_id):
    sys.stdout.write("\033[F")
    print('Getting the list of videos.')
    global item_counter
    for video in page_list['items']:
        item_counter += 1
        id = video['contentDetails']['videoId']

        video_id_list.append(id)

    if 'nextPageToken' in page_list:
        get_playlist_page(playlist_id, page_list['nextPageToken'])

def convert_time(utc_datetime, tz):
    try:
        strip_time = datetime.datetime.strptime(utc_datetime, '%Y-%m-%dT%H:%M:%SZ')
    except:
        strip_time = datetime.datetime.strptime(utc_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_dt = utc.localize(strip_time)
    local_dt = utc_dt.astimezone(tz)
    local_dt = str(local_dt)[:10]
    return local_dt

api_key = sys.argv[1]

max_results = 20
video_id_list = []
video_data = {}
item_counter = 0

scope = input('Would you like to get the metadata of a channel\'s or playlist\'s videos? (Enter "channel" or "playlist"): ').lower().strip()

if scope == 'channel':
    channel_id = input('What is the channel id?: ').strip()
    get_channel_page(channel_id)
elif scope == 'playlist':
    playlist_id = input('What is the playlist id?: ').strip()

    print('\n')

    get_playlist_page(playlist_id)
else:
    print('The scope you entered doesn\'t match the available options. Please use an available option.')
    exit()

print('\nGot a list of ' + str(item_counter) + ' videos.\n')

tz = input('What timezone were the uploads done in? (PST/MST/CST/EST/Other): ').lower().strip()

if tz == 'pst':
    tz = pytz.timezone('US/Pacific')
elif tz == 'mst':
    tz = pytz.timezone('US/Mountain')
elif tz == 'cst':
    tz = pytz.timezone('US/Central')
elif tz == 'est':
    tz = pytz.timezone('US/Eastern')
elif tz == 'other':
    timezone_offset = input('What is the UTC offset of the timezone you wish to use? (Please enter an integer): ').strip()
else:
    print('The timezone you entered doesn\'t match the available options. Please use an available option.')
    exit()

video_counter = 0

print('\n')

for id in video_id_list:
    video_counter += 1
    sys.stdout.write("\033[F")
    print('Getting metadata for video ' + str(video_counter) + ' of ' + str(item_counter) + '.')
    part = 'liveStreamingDetails, snippet, recordingDetails'
    t = requests.get('https://www.googleapis.com/youtube/v3/videos', params={'part':part,'id':id,'key':api_key})

    video = t.json()

    video_data[id] = video['items'][0]

print('')

with open('resource.csv', 'w', newline='') as resource_csv:
    print('Writing out resource.csv.\n')
    rw = csv.writer(resource_csv, delimiter=',')
    header = [
        'aviary ID',
        'Resource User Key',
        'Title',
        'Public',
        'Featured',
        'Description',
        'Date',
        'Agent',
        'Coverage',
        'Language',
        'Format',
        'Type',
        'Subject',
        'Identifier',
        'Custom Unique Identifier',
        'Relation',
        'Source',
        'Publisher',
        'Rights Statement',
        'Keyword',
        'Preferred Citation',
        'Source Metadata URI'
    ]

    rw.writerow(header)

    resource_key = 1

    for video in video_data:
        aviary_id = None
        resource_user_key = resource_key
        title = video_data[video]['snippet']['title']
        public = 'no'
        featured = 'no'
        description = video_data[video]['snippet']['description']
        try:
            date = video_data[video]['recordingDetails']['recordingDate'][:10]
        except:
            try:
                youtube_date = video_data[video]['liveStreamingDetails']['actualStartTime']
            except:
                youtube_date = video_data[video]['snippet']['publishedAt']
            date = convert_time(youtube_date, tz)
        agent = None
        try:
            coverage = 'Place of recording;; ' + video_data[video]['recordingDetails']['locationDescription']
        except:
            coverage = None
        language = None
        video_format = 'Video'
        video_type = None
        subject = None
        identifier = None
        custom_unique_identifier = None
        relation = None
        source = None
        publisher = None
        rights_statement = None
        try:
            keyword_list = video_data[video]['snippet']['tags']
            keyword = '|'.join(keyword_list)
        except:
            keyword = None
        preferred_citation = None
        source_metadata_uri = None
        
        rw.writerow([
            aviary_id,
            resource_user_key,
            title,
            public,
            featured,
            description,
            'Created;; ' + date,
            agent,
            coverage,
            language,
            video_format,
            video_type,
            subject,
            identifier,
            custom_unique_identifier,
            relation,
            source,
            publisher,
            rights_statement,
            keyword,
            preferred_citation,
            source_metadata_uri
        ])

        resource_key += 1

with open('media.csv', 'w', newline='') as media_csv:
    print('Writing out media.csv.\n')
    mw = csv.writer(media_csv, delimiter=',')
    header = [
        'aviary ID',
        'Media User Key',
        'Resource User Key',
        'Path',
        'URL',
        'Embed Code',
        'Embed Source',
        'Target Domain',
        'Sequence #',
        'Public',
        'Media Thumbnail URL',
        'Media Thumbnail Path'
    ]

    mw.writerow(header)

    resource_key = 1
    media_key = 100

    for video in video_data:
        aviary_id = None
        media_user_key = media_key
        resource_user_key = resource_key
        path = None
        url = None
        embed_code = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(video)
        embed_source = 'youtube'
        target_domain = None
        sequence_num = 1
        public = 'Yes'
        media_thumbnail_url = None
        media_thumbnail_path = None
        
        mw.writerow([
            aviary_id,
            media_user_key,
            resource_user_key,
            path,
            url,
            embed_code,
            embed_source,
            target_domain,
            sequence_num,
            public,
            media_thumbnail_url,
            media_thumbnail_path
        ])

        resource_key += 1
        media_key += 1

print('All done!')
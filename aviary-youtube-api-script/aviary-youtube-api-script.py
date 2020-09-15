import requests
import json
import csv

def get_page(page_token=False):
    if page_token:
        r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={'part':part,'maxResults':max_results,'playlistId':playlist_id,'key':api_key, 'pageToken':page_token})
    else:
        r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={'part':part,'maxResults':max_results,'playlistId':playlist_id,'key':api_key})

    response = r.json()

    get_video_id(response)

def get_video_id(page_list):
    global item_counter
    for video in page_list['items']:
        item_counter += 1
        id = video['id']
        part = ['snippet']
        s = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params={'part':part,'id':id,'key':api_key})

        video_dict = s.json()

        video_id_list.append(video_dict['items'][0]['snippet']['resourceId']['videoId'])

    if 'nextPageToken' in page_list:
        get_page(page_list['nextPageToken'])
    else:
        print('There are no more pages')

api_key = 'AIzaSyBLG0DR3ypXsTh06KhpA2kx7qdgQFAj3UY'
playlist_id = 'PLGPrjAxSumLomcPOTfZhbnoLEVZyLSEsK'
max_results = 20
part = 'id'

video_id_list = []

video_data = {}

item_counter = 0

get_page()

print(item_counter)

for id in video_id_list:
    part = 'liveStreamingDetails, snippet'
    t = requests.get('https://www.googleapis.com/youtube/v3/videos', params={'part':part,'id':id,'key':api_key})

    video = t.json()

    video_data[id] = video['items'][0]

with open('resource.csv', 'w', newline='') as resource_csv:
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
        public = 'yes'
        featured = 'no'
        description = video_data[video]['snippet']['description']
        try:
            date = video_data[video]['liveStreamingDetails']['actualStartTime'][:10]
        except:
            date = video_data[video]['snippet']['publishedAt'][:10]
        agent = None
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
        embed_code = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}?cc_load_policy=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(video)
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

# Todo: Add console outpuit
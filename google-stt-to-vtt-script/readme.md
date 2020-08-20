This script converts a folder of Google JSON files to VTT (.vtt) format. Run on 
command line with the following parameters:
- absolute folder path
- (optional) format type ('transcript' for Google's default segmentation or 'fixed_length' for fixed duration--defaults to 'transcript')
- (optional) segment duration (if using 'fixed_length', integer in seconds for desired segment length
example: 'python3 google_stt_to_vtt.py fixed_length 30 "/path/to/my/files/" //breaks out transcript into 30 second segments
example: 'python3 google-stt_to_vtt.py "/path/to/my/files/" //default segments using Google's segmentation
All VTT files are output to a new /vtt directory inside the target folder.

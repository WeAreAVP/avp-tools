# vtt-time-script
The purpose of this script is to adjust the starting time stamp to zero if it is incorrectly offset, and to apply the same change to the remaining timestamps.

Client: Aviary (internal and external as needed). Originally created for use with Austin City Limits' VTTs.

Language: Python
Developed By: David Agudelo-Frankel (@davidagud)

Purpose: 
This script requests a path to a folder with VTTs. The paths can be Windows, Mac, or Linux, and contain spaces. It then creates a new folder within that folder where the time-corrected VTTs will be output.
Next, it loops through all the files in that folder checking the first start time of the VTT, setting it to zero, and subtracting the same amount from all the other time stamps.
Otherwise, the script copies the VTT identically to a new file with the same filename but with "fixed_" appended to the front, and then moves on to the next file.

Requirements: Python 3.x+
Dependencies: None

Usage:
In Terminal or Command Prompt, from the folder where vtt-script.py resides run "python vtt-script.py" or "python3 vtt-script.py" depending on your development configuration.
OR
In Terminal or Command Prompt, run "python [path to vtt-script.py]" or "python3 [path to vtt-script.py]" depending on your development config.

The script will then prompt you for the absolute path to the folder with the VTTs. Note: the script will attempt to parse any files within that folder.
You can type the path or simply drag and drop the folder into Terminal or Command Prompt. Note: the filepath may have spaces. Do not add single quotes around the path, double quotes will be removed by the script.
The adjusted VTTs will be output to a folder within the folder you input into the script. 

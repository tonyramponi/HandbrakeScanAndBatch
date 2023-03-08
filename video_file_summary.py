import subprocess, sys, os, re, shlex, json, csv, os.path, datetime
import errorwindow    

def video_file_summary (file_to_scan, file_data, debug):    
  print(file_to_scan)
  try: 
    p = subprocess.Popen(['ffprobe', '-print_format', 'json', '-show_format', '-show_streams',  file_to_scan], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
  except:
    input("FFprobe ERROR!!!  Press Enter to continue...")    
  
  input_file_ffprobe, err = p.communicate()
  
  # Write out JSON file if debug enabled
  if debug == True:
    dirname,filename = os.path.split(file_to_scan)
    debugfile = open(filename + '.json', "w")
    debugfile.write(input_file_ffprobe.decode('ascii'))
    debugfile.close()
  
  #Get filesize
  size = '0kB'
  size = format((float(os.path.getsize(file_to_scan)) / 1073741824), '.2f')
  file_data.append(size)
  

  # Set variables to store increment of English audio track and subtitle count
  audio_count = 0
  sub_count = 0
  resolution = ('0x0')
  duration = '0:00'
  
  #Import JSON string from captured FFProbe outputs
  try:
    ffprobe_data_decode = json.loads(input_file_ffprobe.decode('UTF-8'))
  except:
    input("ffprobe decode error - press any key")

  if 'streams' in ffprobe_data_decode:
    ffprobe_streams     = ffprobe_data_decode['streams']
  else:
    print ('no streams detected in ' + file_to_scan)
    file_data.append(resolution)
    file_data.append(str(audio_count))
    file_data.append(str(sub_count))
    file_data.append(duration)
    return
  
  # Loop though streams to gather screen res, number of english audio tracks and number of english subtitle tracks
  for stream in range(0, (len(ffprobe_streams))):
    if ffprobe_streams[stream]['codec_type'] == 'video':
      height     = ffprobe_streams[stream]['height']
      width      = ffprobe_streams[stream]['width']
      resolution = str(height) + 'x' + str(width)
      file_data.append(resolution)	  
    elif (ffprobe_streams[stream]['codec_type'] == 'audio' and ffprobe_streams[stream]['tags']['language']  == 'eng'):
      audio_count = audio_count + 1
    elif (ffprobe_streams[stream]['codec_type'] == 'subtitle' and ffprobe_streams[stream]['tags']['language']  == 'eng'):  
      sub_count = sub_count + 1
  file_data.append(str(audio_count))
  file_data.append(str(sub_count))       	
 
  # Get Video file length from "format" part of JSON output 
  if 'format' in ffprobe_data_decode:
    ffprobe_format = ffprobe_data_decode['format']
    seconds = float(ffprobe_format['duration'])
    duration= str(datetime.timedelta(seconds=seconds))
  else:
    print ('no format field detected in ' + file_to_scan)
    file_data.append(duration)
    return
  
  file_data.append(duration)

  return

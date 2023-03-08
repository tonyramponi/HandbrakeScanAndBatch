import subprocess, sys, os, re, shlex, json, csv, os.path, datetime
from Handbrake_batch_maker_list import Handbrake_batch_maker_list
def video_file_summary (file_to_scan, file_data, debug):
  p = subprocess.Popen(['ffprobe', '-print_format', 'json', '-show_format', '-show_streams',  file_to_scan], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
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
  ffprobe_data_decode = json.loads(input_file_ffprobe.decode('ascii'))
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

# Start of main process	  
print ('Video File CSV Comparison creator - T.Barnard 2017')

with open('//wdmycloudex2/Public/python/Video_Comparison/reference_path.txt', 'r') as myfile:
    input_dir=myfile.read().replace('\n', '')

input_dir = input_dir [:-1]
input_dir = input_dir + '\\'
print(input_dir)


with open('//wdmycloudex2/Public/python/Video_Comparison/reference_path2.txt', 'r') as myfile:
    output_dir=myfile.read().replace('\n', '')
output_dir = output_dir [:-1]
output_dir = output_dir + '\\'
print(output_dir)

# Check if input path exists
if os.path.isdir(str(input_dir)):
  print ('Input Directory = ' + input_dir)
else:
  print ('Error - Input path does not exist')
  quit()
  
# Check if output path exists
if os.path.isdir(str(output_dir)):
  print ('Output Directory = ' + output_dir)
else:
  print ('Error - Output path does not exist')
  quit()

# open files 
debugfile = open('//wdmycloudex2/Public/python/Video_Comparison/debug.txt', "w")    # Output Batch file
output_csv = open('//wdmycloudex2/Public/python/Video_Comparison/ffprobe_compare.csv', 'w')
csvwriter = csv.writer(output_csv)
  
# Create List of input files and expected output files from input directory

input_file_list =[]
output_file_list =[]



for dirname, subFolders, files in os.walk(input_dir): # walk though sub directories
  # Create list of input and output files
  for fname in files:
    if ".mkv" or ".mp4" in files:
      input_filename = os.path.join(dirname,fname)
      output_filename = input_filename.replace(input_dir, output_dir)
      input_file_list.append(str(input_filename))
      output_file_list.append(str(output_filename))
   
temp_count = 0 # count vector to output file list

print(input_file_list)
print(output_file_list)

# Write .csv header
output_csv.write('Input_file, output_file_status, compression_ratio, Input_size, Output_size, input_resolution, output_resolution, Input_eng_audio, Output_eng_audio, Input_eng_sub, Input_eng_sub, Input_Duration, Output_Duration ' + '\n')

files_to_compress=[]

for filenames in input_file_list:   # Loop through input file list
  input_file_data  = []
  output_file_data = []

  # Define current input file
  input_file = str(filenames)
  # Define output file based on input file list position
  output_file = str(output_file_list[temp_count])
  # Get input file data using FFProbe procedure
  video_file_summary(input_file, input_file_data, 'false')
  if os.path.isfile(output_file) == True:  # Check if output file exists, If it does continue processing.
    debug = False
    video_file_summary(output_file, output_file_data, debug)
    compression_ratio = format((float(output_file_data[0]) / float(input_file_data[0])) * 100, '.2f')
    compression_ratio_float = float(compression_ratio)
	# check if compression ratio is less than 10%, If it is add it to list to recompress
    if compression_ratio_float < 10:
      files_to_compress.append(filenames)

    report_string = input_file + ', present, ' + compression_ratio + '%, ' + input_file_data[0] + 'GB, ' + output_file_data[0] + 'GB, ' + input_file_data[1] + ', ' + output_file_data[1] + ', ' + input_file_data[2] + ', ' + output_file_data[2] + ', ' + input_file_data[3] + ', ' + output_file_data[3] + ', ' + input_file_data[4] + ', ' + output_file_data[4]
	
  else:                                  # Flag error if output file does not exist 
    report_string = str(filenames) + ', missing' + input_file_data[0] + ', ,'  + input_file_data[1] + ', , ' + input_file_data[2] + ', ,'
    files_to_compress.append(filenames)  
  temp_count = temp_count + 1            # Increment vector for output file list
  output_csv.write(report_string + '\n')  # Write to output file
  	
print (files_to_compress)
debugfile.close()
output_csv.close()
Handbrake_batch_maker_list (files_to_compress, input_dir, output_dir)  	


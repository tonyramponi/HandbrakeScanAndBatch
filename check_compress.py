import subprocess, sys, os, re, shlex, json, csv, os.path, datetime
from video_file_summary import video_file_summary
def check_compress (input_base_path, output_base_path, input_file_list, output_file_list):
  # open files
  try : 
    debugfile = open('//wdmycloudex2/Public/python/Handbrake_batch_maker_MK2/debug.txt', "w")    # Debug file
    output_csv = open('//wdmycloudex2/Public/python/Handbrake_batch_maker_MK2/ffprobe_compare.csv', 'w')
  except:
    input("Error:: Could not open CSV file - Press any key to continue")
  # csvwriter = csv.writer(output_csv)
 
  # Write .csv header
  output_csv.write('Input_file, output_file_status, compression_ratio, Input_size, Output_size, input_resolution, output_resolution, Input_eng_audio, Output_eng_audio, Input_eng_sub, Input_eng_sub, Input_Duration, Output_Duration ' + '\n')
  
  files_to_compress=[]
  
  for filenames in input_file_list:   # Loop through input file list
    input_file_data  = []
    output_file_data = []
  
    # Define current input file
    input_file = str(filenames)
    # Swap out input base path for output base path to check for existance of file
    output_file = input_file.replace(input_base_path, output_base_path)
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
        compression = 'bad'
      else:
        compression = 'good'
  
      report_string = input_file + ', present, ' + compression_ratio + '%, ' + input_file_data[0] + 'GB, ' + output_file_data[0] + 'GB, ' + input_file_data[1] + ', ' + output_file_data[1] + ', ' + input_file_data[2] + ', ' + output_file_data[2] + ', ' + input_file_data[3] + ', ' + output_file_data[3] + ', ' + input_file_data[4] + ', ' + output_file_data[4] + ', ' + compression
  	
    else:                                  # Flag error if output file does not exist 
      report_string = str(filenames) + ', missing' + input_file_data[0] + ', ,'  + input_file_data[1] + ', , ' + input_file_data[2] + ', ,'
      files_to_compress.append(filenames)  
    output_csv.write(report_string + '\n')  # Write to output file
  
  print ("List of missing/incorrect files as follows: - ") 	
  for filenames in files_to_compress:   # Loop through and print missing file list
    print (filenames)
  
  debugfile.close()
  output_csv.close()

  return(files_to_compress)

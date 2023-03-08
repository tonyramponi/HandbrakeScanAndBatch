import subprocess, sys, os, re, shlex, json, csv, os.path, datetime
def create_file_list (input_dir, output_dir):

  # Start of main process	  
  print ('Create File lists')
  
  print(input_dir)
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
     
  
  print(input_file_list)
  print(output_file_list)

  return input_file_list, output_file_list
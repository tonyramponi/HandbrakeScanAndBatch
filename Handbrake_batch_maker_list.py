import subprocess, sys, os, re, shlex, json, csv, os.path
print ('Handbrake batch file creator - T.Barnard 2017')

def Handbrake_batch_maker_list (input_file_list, input_path, output_path):
  
  # Check if output path exists
  if os.path.isdir(str(output_path)):
    print ('Output Directory = ', str(output_path))
  else:
    print ('Error - Output path does not exist')
    quit()
  
  # open files 
  batchfile = open('//wdmycloudex2/Public/python/Video_Comparison/batch_encode.bat', "w")    # Output Batch file
  batchfile.write('powercfg /s 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c\n')
  # Create List of files from input directory
  for dirname, subFolders, files in os.walk(input_path):
    # check if sub directories exist on output path,  Add command to create directory if subfolders do not exist
    for subFoldersname in subFolders:
     Full_path = os.path.join(output_path, subFoldersname)
     if os.path.isdir(Full_path):
       print ('Output sub directory ' + Full_path + ' exists')
     else:
       outputsubdir = 'mkdir "' + str(os.path.join(str(output_path),dirname, subFoldersname))
       outputsubdir = outputsubdir.replace(str(input_path), str(output_path))
       batchfile.write(outputsubdir + '"\n')
  	   		
  print (input_file_list)
  
  # Specify outout path
  path_out = str(output_path)
  
  # Perform FFprobe on each .mkv file in every sub-directory
  for files in input_file_list:
    if ".mkv" in files:
      
      #Detemine full path of file
      #full_file_path = str(input_path) + '\\' + files
      full_file_path = files
  	
      # Invoke FFProbe, capture output and any errors
      p = subprocess.Popen(['ffprobe', '-print_format', 'json', '-show_format', '-show_streams',  full_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
      out, err = p.communicate()
      
      # create empty list for audio tracks
      AudioTrackList = []
  
      # create empty list for subtitles  tracks
      SubTrackList = []
  	
      #Import JSON string
      FfprobeJsonParsed = json.loads(out.decode('ascii'))
  
      subtitle_count = 1
      # Convert to .csv
      print(FfprobeJsonParsed['format']['filename'])
      filename = (FfprobeJsonParsed['format']['filename'])
      VideoData = FfprobeJsonParsed['streams']
      print(len(VideoData), ' streams detected')
      forced_subtitles = False
      for stream in range(0, (len(VideoData))):
        if VideoData[stream]['codec_type'] == 'video':
          print( VideoData[stream]['index'], VideoData[stream]['codec_type'], VideoData[stream]['codec_name'], VideoData[stream]['height'], VideoData[stream]['width'], VideoData[stream]['display_aspect_ratio'], VideoData[stream]['sample_aspect_ratio'])
          videotrack = stream
          if VideoData[stream]['height'] == 1080:
            quality = 22
          else:
            quality = 20
        if (VideoData[stream]['codec_type'] == 'audio' and VideoData[stream]['tags']['language']  == 'eng'):
          print(VideoData[stream]['index'], VideoData[stream]['codec_type'], VideoData[stream]['codec_name'], VideoData[stream]['channels'],VideoData[stream]['tags']['language']  )
          # add to list of audio tracks
          AudioTrackList.append(stream)
          
        if (VideoData[stream]['codec_type'] == 'subtitle' and VideoData[stream]['tags']['language']  == 'eng'):
          print(VideoData[stream]['index'], VideoData[stream]['codec_type'], VideoData[stream]['disposition']['forced'],VideoData[stream]['tags']['language']  )
          forced_subtitle_track = 0
          forced_subtitles = False
          # Set flag for forced sub-titles
          if VideoData[stream]['disposition']['forced'] == 1:
            forced_subtitles = True
            forced_subtitle_track = str(subtitle_count)
          # add to list of subtitle tracks
          SubTrackList.append(subtitle_count)
        if (VideoData[stream]['codec_type'] == 'subtitle'):
          subtitle_count = subtitle_count + 1
      # Print tracks to be processed
      print('Video Track = ', videotrack)	
      print('English Audio Tracks = ', AudioTrackList)
   	
  	# convert subtitle List to string
      SubTrackString = ''
  	
      for p in range(0, len(SubTrackList)): SubTrackString = SubTrackString + str(SubTrackList[p]) + ','
      print(SubTrackString)
      print('English Subtitle Tracks = ', SubTrackList ) 
      
      # Create subtitle string
      if len(SubTrackList) == 0:
        subtitle_command = ''
      else:
        subtitle_command = '--subtitle ' + SubTrackString
      # Add quotes around filename
      filename = '"' + str(filename) + '"'
  	
      # Set output filename, replace base input path with base output path
      filenameout = filename.replace(str(input_path), str(output_path))
      
  	# Generate Handbrake command line
      if forced_subtitles == True:
        print ('handbrakecli --input ' + str(filename) + ' --output ' + str(filenameout) +  ' --format mkv --markers --encoder qsv_h264 --x264-preset balanced --quality ' + str(quality) + ' --audio-lang-list eng --all-audio --aencoder copy ' + subtitle_command + '--subtitle-forced '+ forced_subtitle_track + '\n')
        batchfile.write('handbrakecli --input ' + str(filename) + ' --output ' + str(filenameout) +  ' --format mkv --markers --encoder qsv_h264 --x264-preset balanced --quality ' + str(quality) + ' --audio-lang-list eng --all-audio --aencoder copy ' + subtitle_command + '--subtitle-forced '+ forced_subtitle_track + '\n')
      else:
        print ('handbrakecli --input ' + str(filename) + ' --output ' + str(filenameout) +  ' --format mkv --markers --encoder qsv_h264 --x264-preset balanced --quality ' + str(quality) + ' --audio-lang-list eng --all-audio --aencoder copy ' + subtitle_command +'\n')
        batchfile.write('handbrakecli --input ' + str(filename) + ' --output ' + str(filenameout) +  ' --format mkv --markers --encoder qsv_h264 --x264-preset balanced --quality ' + str(quality) + ' --audio-lang-list eng --all-audio --aencoder copy ' + subtitle_command +'\n')
  batchfile.write('powercfg /s 381b4222-f694-41f0-9685-ff5bb260df2e\n')  
  batchfile.close()
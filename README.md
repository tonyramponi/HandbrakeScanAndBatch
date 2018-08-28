This is work in progress - It works for my specific circumstances but needs development.

# HandbrakeScanAndBatch - What it does
Slightly funky bespoke Python script which takes an input directory containing uncompressed .mkv files and compares it to an output directory containing compressed .mkv files.  The script uses ffprobe to scan the files in both directories and generate a .csv file which shows matching files, the size of the files and the sub-tracks in the files.  The idea is that this .csv comparison can be used as a check 
that a handbrake compression has worked correctly.  If any files are missing from the output directory (i.e. there are new files in the input directory) or there is something fishy in an output file then the script creates a new batch file which will compress the missing/broken files.

# Prerequisites
ffprobe (Part of FFmepeg) and HandbrakeCLI (Handbrake command line Interface) must be installed and on the system path

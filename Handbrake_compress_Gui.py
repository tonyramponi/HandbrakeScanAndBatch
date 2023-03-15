#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from Handbrake_batch_maker_list import Handbrake_batch_maker_list
from video_file_summary import video_file_summary
from check_compress import check_compress
from create_file_list import create_file_list
import errorwindow    

# ******************************************************************************************************************************
# Lists
# ******************************************************************************************************************************
encoder_settings_lists = ["svt_av1", "svt_av1_10bit", "x264", "x264_10bit", "qsv_h264", "x265", "x265_10bit","x265_12bit", "qsv_h265", "qsv_h265_10bit", "mpeg4", "mpeg2", "VP8", "VP9", "VP9_10bit", "theora", "nvenc_h264", "nvenc_h265", "nvenc_h265_10bit"]

# ******************************************************************************************************************************
# Front End Menu Class
# ******************************************************************************************************************************

class start(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.title = "HandBrake Script Generator 4K - TRB 2023"
        self.create_widgets()

    def create_widgets(self):
        rowpos = 1
        self.letsGo = tk.Button(self)
        self.letsGo["text"] = "Compare Folder Content"
        self.letsGo["command"] = self.CompareFolder  
        self.letsGo.grid(row=rowpos,column=1)

        self.generateScript = tk.Button(self)
        self.generateScript["text"] = "Generate Script"
        self.generateScript["command"] = self.genScript  
        self.generateScript.grid(sticky="W",row=rowpos,column=2)

        rowpos = rowpos+1

        self.loadCompareCSV = tk.Button(self)
        self.loadCompareCSV["text"] = "load compare spreadsheet"
        self.loadCompareCSV["command"] = self.loadCompareCSV  
        self.loadCompareCSV.grid(sticky="W",row=rowpos,column=1)

        self.runCompress = tk.Button(self)
        self.runCompress["text"] = "Run Compress"
        self.runCompress["command"] = self.compress  
        self.runCompress.grid(sticky="W",row=rowpos,column=2)

        rowpos = rowpos+1
        self.sdsettings = tk.Label(self)
        self.sdsettings["text"] = "SD Settings"
        self.sdsettings.grid(row=rowpos,column=1)
        self.sd_encoder = ttk.Combobox(self)
        #self.sd_encoder.geometry("300x250")
        self.sd_encoder.grid(row=rowpos,column=2)
        for item in encoder_settings_lists:
          self.sd_encoder['values'] = (*self.sd_encoder['values'], item)
        
        #self.sd_encoder.insert(1, "svt_av1")
        #self.sd_encoder.insert(2, "svt_av1_10bit")
        #self.sd_encoder.insert(3, "x264")
        #self.sd_encoder.insert(4, "x264_10bit")

        rowpos = rowpos+1

        self.outputFormat = tk.Checkbutton(self)
        self.outputFormat["text"] = "mp4"
        self.outputFormat["variable"] = self.outputFormat  
        self.outputFormat.grid(sticky="W",row=rowpos,column=1)


        self.chkValue = tk.BooleanVar() 
        self.chkValue.set(False)
        self.x265 = tk.Checkbutton(self)
        self.x265["text"] = "h265"
        self.x265["variable"] = self.chkValue
        self.x265.grid(sticky="W",row=rowpos,column=2)


        rowpos = rowpos + 1
        self.scriptNamelab = tk.Label(self)
        self.scriptNamelab["text"] = "Script Name"
        self.scriptNamelab.grid(row=rowpos,column=1)
        self.scriptName = tk.Entry(self, width=150)
        self.scriptName.grid(row=rowpos,column=2)
        self.scriptName.insert(0, "\\\\wdmycloudex2\\Public\\python\\Handbrake_batch_maker_MK2\\batch_encode.bat")
        
        rowpos = rowpos + 1
        self.inputPathlab = tk.Label(self)
        self.inputPathlab["text"] = "Input Path"
        self.inputPathlab.grid(row=rowpos,column=1)
        self.inputPath = tk.Entry(self, width=150)
        self.inputPath.grid(row=rowpos,column=2)
        self.inputPath.insert(0, "H:\\BluRay_in\\ready_to_scan")

        rowpos = rowpos + 1
        self.outputPathlab = tk.Label(self)
        self.outputPathlab["text"] = "Output Path"
        self.outputPathlab.grid(row=rowpos,column=1)
        self.outputPath = tk.Entry(self, width=150)
        self.outputPath.grid(row=rowpos,column=2)
        self.outputPath.insert(0, "H:\\Handbrake_out\\newfilms")

    def CompareFolder(self):
      input_file_list, output_file_list = create_file_list(self.inputPath.get(),self.outputPath.get())
      files_to_compress = check_compress(self.inputPath.get(),self.outputPath.get(),input_file_list, output_file_list)

    def genScript(self):
      input_file_list, output_file_list = create_file_list(self.inputPath.get(),self.outputPath.get())
      files_to_compress = check_compress(self.inputPath.get(),self.outputPath.get(),input_file_list, output_file_list)
      x265 = self.chkValue.get()
      print (str(x265))
      run_compress = False
      Handbrake_batch_maker_list (files_to_compress, self.inputPath.get(),self.outputPath.get(),self.scriptName.get(), x265, run_compress)

    def compress(self):
      input_file_list, output_file_list = create_file_list(self.inputPath.get(),self.outputPath.get())
      files_to_compress = check_compress(self.inputPath.get(),self.outputPath.get(),input_file_list, output_file_list)
      print ('Number of files to compress =' + str(len(files_to_compress)))
      loop_count = 0
      while (len(files_to_compress) > 0) and (loop_count < 6):
        x265 = self.chkValue.get()
        print (str(x265))
        run_compress = True
        Handbrake_batch_maker_list (files_to_compress, self.inputPath.get(),self.outputPath.get(),self.scriptName.get(), x265, run_compress)
        files_to_compress = check_compress(self.inputPath.get(),self.outputPath.get(),input_file_list, output_file_list)
        if loop_count == 5:
          print('Too many attempts to compress - Exiting')
        loop_count = loop_count + 1

root = tk.Tk()
app = start(master=root)
root.mainloop()

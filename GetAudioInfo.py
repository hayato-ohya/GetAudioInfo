#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:46:37 2018

@author: Hayato Ohya
"""
import os
import re
import subprocess

class GetAudioInfo(object):
    def __init__(self, audioPath):
        self.major_brand = None
        self.minor_version = None
        self.compatible_brands = None
        self.creation_time = None
        self.sort_album_artist = None
        self.copyright_eng = None
        self.title = None
        self.artist = None
        self.album_artist = None
        self.album = None
        self.date = None
        self.track = None
        self.disc = None
        self.composer = None
        self.sort_name = None
        self.sort_artist = None
        self.copyright = None
        self.duration = None
        self.bitrate = None
        self.sampling_rate = None
        self.channel_type = None
        self.audio_type = None
        
        if (os.path.isfile(audioPath)):
            cmd = "avprobe -hide_banner " + audioPath # ffmpeg and avprobe must be installed.
            out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if (out.returncode != 0):
                cmd = "avprobe " + audioPath
            out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = out.stdout
            out_decoded = out.decode().split("\n")
            
            # Search for "Metadata"
            metadataFlg = False
            for i, elem in enumerate(out_decoded):
                if re.search("Metadata", elem) is not None:
                    metadataFlg = True
                elif metadataFlg: # after "Metadata"
                    break
            
            # member valiable
            self.extension = cmd.split(".")[-1]
            try:
                while True:
                    if out_decoded[i].split(": ")[0].replace(" ","") == "major_brand":
                        self.major_brand = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "minor_version":
                        self.minor_version = int(out_decoded[i].split(": ")[1])
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "compatible_brands":
                        self.compatible_brands = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "creation_time":
                        self.creation_time = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "sort_album_artist":
                        self.sort_album_artist = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "copyright-eng":
                        self.copyright_eng = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "title":
                        self.title = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "artist":
                        self.artist = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "album_artist":
                        self.album_artist = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "album":
                        self.album = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "date":
                        self.date = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "track":
                        self.track = int(out_decoded[i].split(": ")[1])
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "disc":
                        self.disc = int(out_decoded[i].split(": ")[1])
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "composer":
                        self.composer = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "sort_name":
                        self.sort_name = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "sort_artist":
                        self.sort_artist = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "copyright":
                        self.copyright = out_decoded[i].split(": ")[1]
                    elif out_decoded[i].split(": ")[0].replace(" ","") == "Duration":
                        self.duration = out_decoded[i].split(": ")[1].split(", ")[0]
                        self.bitrate = out_decoded[i].split(": ")[3]
                        self.audio_type = out_decoded[i+1].split(", ")[0].split(": ")[2].split(" (")[0]
                        if len(out_decoded[i+1].split(", ")) == 1:
                            self.sampling_rate = int(out_decoded[i+2].split(", ")[0].replace(" ","").replace("Hz",""))
                            self.channel_type = out_decoded[i+2].split(", ")[1]
                        else:
                            self.sampling_rate = int(out_decoded[i+1].split(", ")[1].split(" ")[0])
                            self.channel_type = out_decoded[i+1].split(", ")[2]
                    else:
                         break   
                    i += 1
            except IndexError:
                print("==IndexError==")
            
        else:
            print(audioPath + " doesn't exist.")
        
    def convertDict(self):
        audioInfo = {"major_brand" : self.major_brand,
                         "minor_version" : self.minor_version,
                         "compatible_brands" : self.compatible_brands,
                         "creation_time" : self.creation_time,
                         "sort_album_artist" : self.sort_album_artist,
                         "copyright-eng" : self.copyright_eng,
                         "title" : self.title,
                         "artist" : self.artist,
                         "album_artist" : self.album_artist,
                         "album" : self.album,
                         "date" : self.date,
                         "track" : self.track,
                         "disc" : self.disc,
                         "composer" : self.composer,
                         "sort_name" : self.sort_name,
                         "sort_artist" : self.sort_artist,
                         "copyright" : self.copyright,
                         "duration" : self.duration,
                         "bitrate" : self.bitrate,
                         "sampling_rate" : self.sampling_rate,
                         "channel_type" : self.channel_type,
                         "audio_type" : self.audio_type,
                         "extension" : self.extension}
        return audioInfo
    
#audioPath = "/Users/h-oya/Downloads/8134082.m4a"
#audioInfo = GetAudioInfo(audioPath)
#audioDict = GetAudioInfo.convertDict(audioInfo)
#for elem in audioDict:
#    print(elem + ": " + str(audioDict[elem]))


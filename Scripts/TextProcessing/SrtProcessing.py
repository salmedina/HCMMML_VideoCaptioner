import os
import collections

MovieInfo = collections.namedtuple('MovieInfo', 'filename times caption')

def get_video_clips(srtFileName):
    fileList = []
    if os.path.isfile(srtFileName):
        srtLines = open(srtFileName,'r').readlines()
        fileList = [srtLines[i] for i in range(0,len(srtLines),4)]
    
    return fileList

def get_times(srtFileName):
    timesList = []
    if os.path.isfile(srtFileName):
        srtLines = open(srtFileName,'r').readlines()
        timesList = [srtLines[i] for i in range(1,len(srtLines),4)]
    
    return timesList

def get_captions(srtFileName):
    captionSentences = []
    if os.path.isfile(srtFileName):
        srtLines = open(srtFileName,'r').readlines()
        captionSentences = [srtLines[i] for i in range(2,len(srtLines),4)]
    
    return captionSentences

def get_movie_info(srtFileName):
    fileList = get_video_clips(srtFileName)
    durationList = get_durations(srtFileName)
    captionsList = get_captions(srtFileName)
    return zip(fileList, durationList, captionsList)

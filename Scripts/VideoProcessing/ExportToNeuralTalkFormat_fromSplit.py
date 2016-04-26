
#!/usr/bin/env python

import os
import re
import cv2
import json
import argparse
from os.path import basename, dirname, join, splitext
import pickle as pkl
import pdb
import MySQLdb as sql

VIDEO_FPS = 30

class NTSettings:
    file_list = []
    output_dir = ''
    sample_rate = ''
    frame_height = ''
    frame_width = ''
    
    def __init__(self, file_list = [], output_dir='', sample_rate='', frame_height='', frame_width='', num_frames = 10):
        self.file_list = file_list
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.num_frames = num_frames

def build_video_path(base_path, video_name):
    movie_name = re.search(r'(.*)_DVS\d*.avi', video_name).group(1)
    return os.path.join(base_path, movie_name,'video',video_name)

def sample_frames(video_filepath, start_frame, end_frame, output_path, \
                  sample_rate, frame_height, frame_width):
    '''Returns the list of extracted frames file paths'''
    
    #Initialize the video capture
    vid_cap = cv2.VideoCapture(video_filepath)
    ret,cur_frame = vid_cap.read()
    if not ret:
        print 'ERROR, could not open video file'
        return
    frame_pos = 1
    
    #Break-down the video path
    video_dir = dirname(video_filepath)
    video_name, video_ext = splitext(basename(video_filepath))
    video_file_base = splitext(video_filepath)
    
    #Calculate the frame positions which will be extracted
    # FrameRate/SampleRate = Frames/s / NumSample/s = Frames/NumSamples = FrameSpan
    extract_pos = range(start_frame, end_frame, int(VIDEO_FPS/sample_rate))
    captured_img_ext = '.png'
    captured_img_list = []
    
    #Scan all the frames
    while frame_pos < end_frame or ret:
        ret, cur_frame = vid_cap.read()
        frame_pos += 1
        #And capture only the ones we care of
        if frame_pos in extract_pos:
            tmp_img_capture_path = join(output_path,'%s_%05d%s'%(video_name, frame_pos, captured_img_ext))
            cv2.imwrite(tmp_img_capture_path, cv2.resize(cur_frame, (frame_width, frame_height)))
            captured_img_list.append(tmp_img_capture_path)
    
    return captured_img_list

def extract_frames(file_list, output_dir, sample_rate, frame_height, frame_width, num_frames, base_path):
    '''Returns a list of captions with their respective list of images (caption, [list of images])'''
    ## connect to the database
    db = sql.connect("atlas4.multicomp.cs.cmu.edu","annotator","multicomp","annodb")
    
    cursor = db.cursor()

    img_caption_list = []
    for movie in file_list:
        sq1 = "select text, video_name, video_path from captions where movie = \'%s\'" %(movie)
        cursor.execute(sq1)
        tuples = cursor.fetchall()
        for tup in tuples:
            caption = tup[0]
            video_filename = tup[1]
            video_path = os.path.join(base_path,tup[2])
            start_frame = 1
            pdb.set_trace()
            ## for end_frame we need to find that from allvideos table
            #sq2 = "select length from allvideos where video_name = \'%s\'" %(video_filename)
        
            captured_frames_list = sample_frames(video_path, int(start_frame), int(end_frame), output_dir, \
                                                 sample_rate, frame_height, frame_width)
            #TODO: fix this memory bloat
            n_captions = [caption]*len(captured_frames_list)
            img_caption_list += zip(captured_frames_list, n_captions)
        
    return img_caption_list
    
def export_to_neuraltalk(extraction_list, output_file):
    '''Converts the extraction to NeuralTalk import JSON file '''
    
    export_dict = {}
    for image, caption in extraction_list:
        
        export_dict[image] = caption
    json.dump(export_dict, open(output_file, 'w'), indent=4)

if __name__=='__main__':
    
    split_list = pkl.load(open('split_list.p','rb'))
    settings = NTSettings()
    settings.file_list = split_list[0] + split_list[1] + split_list[2]
    settings.output_dir = './KeyFrames'
    settings.sample_rate = 7
    settings.frame_height = 240
    settings.frame_width = 427
    settings.num_frames = 10
    settings.output_file = 'mixed.json'
    settings.base_path = '/multicomp/datasets/'
    #extraction list 
    extraction_list = extract_frames(settings.file_list, \
                                     settings.output_dir, \
                                     settings.sample_rate, \
                                     settings.frame_height,\
                                     settings.frame_width, \
                                     settings.num_frames, \
                                     settings.base_path)
    
    export_to_neuraltalk(extraction_list, settings.output_file)

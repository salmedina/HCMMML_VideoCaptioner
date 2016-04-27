
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
import numpy as np
import subprocess as sp
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

def get_total_frames(video_file_path):
    video_capture = cv2.VideoCapture(video_file_path)
    ret, cur_frame = video_capture.read()
    total_frames = 0
    while ret:
        total_frames += 1
        ret, cur_frame = video_capture.read()
        if not ret:
            break
    return total_frames

    
def sample_frames(video_filepath, start_frame, end_frame, output_path, \
                  sample_rate, frame_height, frame_width, num_frames):
    '''Returns the list of extracted frames file paths'''
    
    #Initialize the video capture
    vid_cap = cv2.VideoCapture(video_filepath)
    ret,cur_frame = vid_cap.read()
    if not ret:
        print 'ERROR, could not open video file'
        return
    frame_pos = 0
    
    #Break-down the video path
    video_dir = dirname(video_filepath)
    video_name, video_ext = splitext(basename(video_filepath))
    video_file_base = splitext(video_filepath)
    
    #Calculate the frame positions which will be extracted
    # FrameRate/SampleRate = Frames/s / NumSample/s = Frames/NumSamples = FrameSpan
    step_size = int(np.ceil((end_frame-start_frame-1)/num_frames))
    extract_pos = []
    sum_frames = start_frame
    for count in range(num_frames):
        extract_pos += [sum_frames]
        sum_frames += step_size
    captured_img_ext = '.png'
    captured_img_list = []

    print len(extract_pos)
    if (len(extract_pos) !=10):
        pdb.set_trace()
    
    #Scan all the frames
    while frame_pos < end_frame or ret:
        ret, cur_frame = vid_cap.read()
        frame_pos += 1
        #And capture only the ones we care of
        if frame_pos in extract_pos:
            tmp_img_capture_path = join(output_path,'%s_%05d%s'%(video_name, frame_pos, captured_img_ext))
            try:
                cv2.imwrite(tmp_img_capture_path, cv2.resize(cur_frame, (frame_width, frame_height)))
            except:
                pdb.set_trace()
            captured_img_list.append(tmp_img_capture_path)

            
    return captured_img_list

def extract_frames(file_list, output_dir, sample_rate, frame_height, frame_width, num_frames, base_path):
    '''Returns a list of captions with their respective list of images (caption, [list of images])'''
    ## connect to the database
    db = sql.connect("atlas4.multicomp.cs.cmu.edu","annotator","multicomp","annodb")
    
    cursor = db.cursor()

    img_caption_list = []
    sum_count = 0
    count = 0
    for movie in file_list:
        sq1 = "select count(*) from captions where movie = \'%s\'" %(movie)
        cursor.execute(sq1)
        tuples = cursor.fetchall()
        print tuples
        sq1 = "select text, video_name, video_path,id from captions where movie = \'%s\'" %(movie)
        cursor.execute(sq1)
        tuples = cursor.fetchall()
        print movie
        sum_count += count
        for count,tup in zip(range(len(tuples)),tuples):
            print count+sum_count
            caption = tup[0]
            video_filename = tup[1]
            video_path = os.path.join(base_path,tup[2])
            start_frame = 1

            ## for end_frame we need to find that from allvideos table
#            sq2 = "select id from captions where text = \'%s\'" %(caption)
#            cursor.execute(sq2)
#            caption_id = cursor.fetchall()
            caption_id = int(tup[3])
            end_frame = get_total_frames(video_path)
            captured_frames_list = sample_frames(video_path, int(start_frame), int(end_frame), output_dir, \
                                                 sample_rate, frame_height, frame_width, num_frames)
            #TODO: fix this memory bloat
            n_captions = [caption]*len(captured_frames_list)
            n_caption_id = [caption_id]*len(captured_frames_list)
            img_caption_list += zip(captured_frames_list, n_captions, n_caption_id)

            comm = 'ls %s_* | wc -l' %(os.path.join(output_dir,video_filename))
            num_files_written = int(sp.check_output(['bash','-c',comm]))
            if (num_files_written != 10):
                pdb.set_trace()

            
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
#    settings.file_list = settings.file_list[19:]
    settings.output_dir = './KeyFramesFinal'
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
    pkl.dump(extraction_list,open('mixed.p','wb'))
    export_to_neuraltalk(extraction_list, settings.output_file)

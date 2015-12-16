#!/usr/bin/env python

import os
import re
import sys
import cv2
import json
import nltk
import argparse
import cPickle as pickle
from nltk.tokenize import sent_tokenize
from os.path import basename, dirname, join, splitext

VIDEO_FPS = 30

class NTSettings:
    source_videos_dir = ''
    annotation_file = ''
    output_dir = ''
    nt_output_file = ''
    sample_rate = ''
    frame_height = ''
    frame_width = ''
    
    def __init__(self, source_videos_dir='', annotation_file='', output_dir='', sample_rate='', frame_height='', frame_width='', nt_output_file=''):
        self.source_videos_dir = source_videos_dir
        self.annotation_file = annotation_file
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        self.frame_height = frame_height
        self.frame_width = frame_width
        self.nt_output_file = nt_output_file
        
def get_total_frames(video_path):
    if not os.path.isfile(video_path):
        return 0
    
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        return 0
    
    total_frames = 0
    ret, fr = vidcap.read()
    if ret:
        total_frames += 1
    while ret:
        ret, fr = vidcap.read()
        total_frames += 1
        
    return total_frames

def build_video_path(base_path, video_name):
    movie_name = re.search(r'(.*)_DVS\d*.avi', video_name).group(1)
    return os.path.join(base_path, movie_name,'video',video_name)

def get_frames_of_interest(sample_size, start_frame, end_frame):
    segment_len = end_frame - start_frame
    if segment_len < sample_size:
        return range(1,segment_len,1)
    
    skip_size = int(round(segment_len / sample_size))
    padding = int((segment_len%sample_size) / 2)
    start_point = padding
    end_point = segment_len - padding
    
    return range(start_frame+padding, end_frame-padding, skip_size)

def sample_frames(video_path, start_frame, end_frame, output_path, \
                  sample_rate, frame_height, frame_width):
    '''Returns the list of extracted frames file paths'''
    
    #Initialize the video capture
    vid_cap = cv2.VideoCapture(video_path)
    ret,cur_frame = vid_cap.read()
    if not ret:
        print 'ERROR, could not open video file'
        return
    frame_pos = 1
    
    #Break-down the video path
    video_dir = dirname(video_path)
    video_name, video_ext = splitext(basename(video_path))
    video_file_base = splitext(video_path)
    video_len = get_total_frames(video_path)
    
    #Calculate the frame positions which will be extracted
    # FrameRate/SampleRate = Frames/s / NumSample/s = Frames/NumSamples = FrameSpan
    extract_pos = get_frames_of_interest(sample_rate, start_frame, end_frame)
    #TODO: remove a hard coded
    captured_img_ext = '.png'
    captured_img_list = []
    
    #Scan all the frames
    while frame_pos < end_frame or ret:
        ret, cur_frame = vid_cap.read()
        frame_pos += 1
        #And capture only the ones we care of
        if frame_pos in extract_pos:
            img_capture_filename = '%s_%05d%s'%(video_name, frame_pos, captured_img_ext)
            tmp_img_capture_path = join(output_path,img_capture_filename)
            if not os.path.isfile(tmp_img_capture_path):
                cv2.imwrite(tmp_img_capture_path, cv2.resize(cur_frame, (frame_width, frame_height)))
            #List of image base names, the path was given from the user
            captured_img_list.append(img_capture_filename)
    
    return captured_img_list

def extract_frames(videos_dir, annotation_file, output_dir, sample_rate, frame_height, frame_width):
    '''Returns a list of captions with their respective list of images (caption, [list of images])'''
    #Open the annotations file
    annotation_list = open(annotation_file, 'r').readlines()
    
    img_caption_list = []
    annotation_count = 0
    for annotation in annotation_list:
        #TODO: there are captions that have tab, clean up from dictionaries and srt's
        anno_fields = annotation.split('\t')
        video_filename = anno_fields[0]
        start_frame = anno_fields[1]
        end_frame = anno_fields[2]
        caption = anno_fields[3]
        
        caption_list = map(lambda x: x.strip(), sent_tokenize(caption))
        video_path = build_video_path(videos_dir, video_filename)
        
        annotation_count += 1
        print '%d) Extracting frames for: %s'%(annotation_count, video_filename)
        
        captured_frames_list = sample_frames(video_path, int(start_frame), int(end_frame), output_dir, \
                                             sample_rate, frame_height, frame_width)
        #TODO: fix this memory bloat
        n_captions = [(caption_list)]*len(captured_frames_list)
        img_caption_list += zip(captured_frames_list, n_captions)
        
    return img_caption_list
    
def export_to_neuraltalk(extraction_list, output_file):
    '''Converts the extraction to NeuralTalk import JSON file '''
    
    caption_data = []
    for image_filename, captions in extraction_list:
        annotation = {}
        captions = map(lambda x: x.strip(), captions)
        captions = map(lambda x: re.sub(r'[^\x00-\x7f]',r' ',x), captions)
        annotation['captions'] = (captions)
        annotation['file_path'] = image_filename.strip()
        annotation['id'] = os.path.splitext(image_filename.strip())[0]
        caption_data.append(annotation)
    
    json.dump(caption_data, open(output_file, 'w'))

def validate_ntsettings(inSettings):
    if not os.path.isdir(inSettings.source_videos_dir):
        print 'Invalid videos directory'
        return False
    
    if not os.path.isfile(inSettings.annotation_file):
        print 'Invalid annotation csv file'
        return False
    
    if not os.path.isdir(inSettings.output_dir):
        print 'Invalid output directory'
        return False
    
    return True

if __name__=='__main__':
    
    settings = NTSettings()
    
    settings.source_videos_dir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDtranscription'
    settings.annotation_file = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/VideoAnnotation/ActionAnnotations/allActions.csv'
    settings.output_dir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealFullActionFrames'
    settings.nt_output_file = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/VideoAnnotation/ActionAnnotations/allActionsFrames.json'
    settings.sample_rate = 30
    settings.frame_height = 240
    settings.frame_width = 427
    
    if not validate_ntsettings(settings):
        sys.exit(-1)
    
    #extraction list 
    
    extraction_list = extract_frames(settings.source_videos_dir, \
                                     settings.annotation_file, \
                                     settings.output_dir, \
                                     settings.sample_rate, settings.frame_height, settings.frame_width)
    
    pickle.dump(extraction_list, open('extractionList.p', 'w'))
    '''
    extraction_list = pickle.load(open('extractionList.p'))
    export_to_neuraltalk(extraction_list, settings.nt_output_file)
    '''
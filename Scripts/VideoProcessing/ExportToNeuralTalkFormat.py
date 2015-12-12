#!/usr/bin/env python

import os
import re
import cv2
import json
import argparse
from os.path import basename, dirname, join, splitext

VIDEO_FPS = 30

class NTSettings:
    source_videos_dir = ''
    annotation_file = ''
    output_dir = ''
    sample_rate = ''
    frame_height = ''
    frame_width = ''
    
    def __init__(self, source_videos_dir='', annotation_file='', output_dir='', sample_rate='', frame_height='', frame_width=''):
        self.source_videos_dir = source_videos_dir
        self.annotation_file = annotation_file
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        self.frame_height = frame_height
        self.frame_width = frame_width
        

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

def extract_frames(videos_dir, annotation_file, output_dir, sample_rate, frame_height, frame_width):
    '''Returns a list of captions with their respective list of images (caption, [list of images])'''
    #Open the annotations file
    annotation_list = open(annotation_file, 'r').readlines()
    
    img_caption_list = []
    for annotation in annotation_list:
        video_filename, start_frame, end_frame, caption = annotation.split('\t')
        video_path = build_video_path(videos_dir, video_filename)
        
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
        for image in image_list:
            export_dict[image] = caption
    json.dump(export_dict, open(output_file, 'w'), indent=4)

if __name__=='__main__':
    
    settings = NTSettings()
    
    settings.source_videos_dir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDtranscription'
    settings.annotation_file = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/video_action_annotations.csv'
    settings.output_dir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDTranscriptionKeyFrames'
    settings.sample_rate = 15
    settings.frame_height = 240
    settings.frame_width = 427
    
    #extraction list 
    extraction_list = extract_frames(settings.source_videos_dir, \
                                     settings.annotation_file, \
                                     settings.output_dir, \
                                     settings.sample_rate, settings.frame_height, settings.frame_width)
    
    export_to_neuraltalk(extraction_list, settings.output_file)

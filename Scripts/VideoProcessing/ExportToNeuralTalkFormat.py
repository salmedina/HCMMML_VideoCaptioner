#!/usr/bin/env python

import os
import cv2
import json
import argparse
from os.path import basename, dirname, join, splitext

VIDEO_FPS = 30

def build_video_path(base_path, video_name):
    movie_name = re.search(r'(.*)_DVS\d*', video_name).group(1)
    return os.path.join(base_path, movie_name,'video',video_name+'.avi')

def sample_frames(video_filepath, start_frame, end_frame, output_path, \
                  sample_rate, frame_width, frame_height):
    '''Returns the list of extracted frames file paths'''
    
    #Initialize the video capture
    vid_cap = cv2.VideoCapture()
    ret,cur_frame = vid_cap.read(video_filepath)
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
            cv2.imwrite(tmp_img_capture_path, cur_frame)
            captured_img_list.append(tmp_img_capture_path)
    
    return captured_img_list

def extract_frames(videos_dir, annotation_file, output_file):
    '''Returns a list of captions with their respective list of images (caption, [list of images])'''
    #Open the annotations file
    annotation_list = open(annotation_file, 'r').readlines()
    
def export_to_neuraltalk(extraction_list, output_file):
    '''Converts the extraction to NeuralTalk import JSON file '''
    
    export_dict = {}
    for caption,image_list in extraction_list:
        for image in image_list:
            export_dict[image] = caption
    json.dump(export_dict, open(output_file, 'w'), indent=4)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('annotation_file', type=str, help='File that contains the video annotations to be exported to NeuralTalk')
    parser.add_argument('source_videos_dir', type=str, help='Path that contains the Montreal video set')
    parser.add_argument('output_dir', type=str, help='Path where the extracted frames will be stored')
    parser.add_argument('output_file', type=str, help='File path to exported json file')
    parser.add_argument('sample_rate', type=str, help='Frame extraction sample rate')
    parser.add_argument('frame_width', type=int, help='Exported frame width')
    parser.add_argument('frame_height', type=int, help='Exported frame height')
    args = parser.parse_args()
    
    #extraction list 
    extraction_list = extract_frames(args.source_videos_dir, \
                     args.annotation_file, \
                     args.output_dir, \
                     args.sample_rate, args.frame_width, args.frame_height)

    export_to_neuraltalk(extraction_list, args.output_file)

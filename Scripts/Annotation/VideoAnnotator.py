#!/usr/bin/env python
import cv2
import re
import os
import glob
import fileinput
import fnmatch
import pdb
import tty, sys, termios
import select
import pickle
from collections import deque
from collections import namedtuple
from matplotlib import pyplot as plt

class VASettings:
    base_path = ''
    output_path = ''
    video_dir = ''
    movie_dir = ''
    cc_dict_path = ''
    video_list_path = ''
    
    def __init__(self, base_path='', output_path='', movie_dir='', video_dir='', cc_dict_path='', video_list_path=''):
        self.base_path = base_path
        self.output_path = output_path
        self.video_dir = video_dir
        self.movie_dir = movie_dir
        self.cc_dict_path = cc_dict_path
        self.video_list_path = video_list_path

def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)

def build_video_path(base_path, video_name):
    movie_name = re.search(r'(.*)_DVS\d*', video_name).group(1)
    return os.path.join(base_path, movie_name,'video',video_name+'.avi')

def display_video_capture(video_file_path, capture_dir=''):
    #Persist until a video frame is captured
    captured_file_name = ''
    captured_frame = False
    skipped = False
    exit = False
    start_frame = 0
    end_frame = 0
    video_filename = os.path.basename(os.path.splitext(video_file_path)[0])
    while not captured_frame and not skipped and not exit:
        # start the video capture objec
        # Player variables
        video_paused = False
        inbuffer_index = 0
        frame_buffer = deque(maxlen=60)
        # Initialize video capture object
        video_capture = cv2.VideoCapture(video_file_path)
        ret, cur_frame = video_capture.read()
        if ret:
            frame_pos = 1
            frame_buffer.append((frame_pos, cur_frame))
        #While videocapture keeps on throwing videos
        while ret:
            if not video_paused:
                if inbuffer_index < 0:   #we are reading from buffer
                    _, cur_frame = frame_buffer[inbuffer_index]
                    inbuffer_index += 1
                else:
                    ret, cur_frame = video_capture.read()
                    frame_pos += 1  #always show from frame 2
                    frame_buffer.append((frame_pos, cur_frame))
            if ret:
                # Show the frame
                cv2.imshow(video_filename, cur_frame)

                # Monitor keyboard input
                key = cv2.waitKey(33) #33 [ms] to achieve ~30 FPS

                if key == 32:  # SPACE: Toggle PAUSE / PLAY
                    video_paused = not video_paused
                    
                elif key == ord('n') or key == ord('N'):  # STEP BACK
                    video_paused = True
                    if len(frame_buffer) > 0 and len(frame_buffer)+inbuffer_index > 1:
                        inbuffer_index -= 1
                        _,cur_frame = frame_buffer[inbuffer_index]
                        
                elif key == ord('m') or key == ord('M'):  # STEP FORWARD
                    video_paused = True
                    if inbuffer_index < -1: #we are navigating within the buffer
                        inbuffer_index += 1
                        _,cur_frame = frame_buffer[inbuffer_index]
                    else:
                        inbuffer_index = 0
                        ret, cur_frame = video_capture.read()
                        frame_pos += 1  #always show from frame 2
                        frame_buffer.append((frame_pos, cur_frame))
                        
                elif key == ord('.'): # Store frame
                    # Capture current frame
                    if capture_dir is not '':
                        captured_file_name = video_file_path[0:len(video_file_path)-4] + '_%05d' %(frame_pos+inbuffer_index) + '.png'
                        print "Saving frame %s"%(captured_file_name)
                        cv2.imwrite(os.path.join(capture_dir,captured_file_name),cur_frame)
                    captured_frame = True
                    break
                
                elif key == ord('x') or key == ord('X'):    # Set START point
                    start_frame = frame_pos+inbuffer_index
                    if end_frame < start_frame:
                        end_frame = start_frame
                    print 'IN: %d     OUT: %d'%(start_frame, end_frame)
                    
                elif key == ord('c') or key == ord('C'):    # Set STOP point
                    end_frame = frame_pos+inbuffer_index
                    if start_frame > end_frame:
                        start_frame = end_frame
                    print 'IN: %d     OUT: %d'%(start_frame, end_frame)
                    
                elif key == ord('j') or key == ord('J'):    # JUMP to next file
                    captured_frame = True
                    break
                elif key == 27 or key == 'q' or key == 'Q': # ESC: exit program 
                    cv2.destroyWindow(video_filename)
                    exit = True
                    break
                
        cv2.destroyWindow(video_filename)
    
    return exit, skipped, start_frame, end_frame, captured_file_name

def capture_movie_frames(base_path, path1, path2, out_path, cc_dict_path):
    '''
    All the videos in the paths are shown to the user
    The player allows through keyboard input to play/pause and capture the video
    '''
    #Load the captions dictionary
    cc_dict = None
    if os.path.isfile(cc_dict_path):
        cc_dict = pickle.load(open(cc_dict_path, 'rb'))
    
    # make the output path if it does not exist
    if not os.path.isdir(os.path.join(out_path,path1)):
        os.makedirs(os.path.join(out_path,path1))
    
    #Go through all the video files in the folder
    for video_filename in os.listdir(os.path.join(base_path,path1,path2)):
        #We are only interested in the AVI video files
        if fnmatch.fnmatch(video_filename,'*.avi'):
            #If already screen capped, go to next file
            video_basename = os.path.splitext(os.path.basename(video_filename))[0]
            if len(glob.glob(os.path.join(out_path,path1)+'/'+video_basename+'*.png')) > 0:
                continue
            
            print video_filename
            if cc_dict is not None:
                video_filename_no_ext = os.path.splitext(video_filename)[0]
                if video_filename_no_ext in cc_dict:
                    print 'Seeking frame for'
                    print cc_dict[video_filename_no_ext]
                    video_file_path = os.path.join(base_path,path1,path2,video_filename)
                    display_video_capture(video_file_path, out_path)

def annotate_movie_times(base_path, video_list_path, cc_dict_path, annotations_path):
    '''
    All the vidoes in the movie_path_list are shown to the user
    The player allows through keyboard input to play/pause, capture the video and set start/end times
    '''
    #Get list of videos from file
    video_list = open(video_list_path).readlines()
    video_list = map(lambda x:x.strip(), video_list) #clean all the \r, \n, spaces, etc
    #Load the captions dictionary
    cc_dict = pickle.load(open(cc_dict_path))
    #Annotation definition
    #is a tuple with (video_name, in, out, caption)
    annotated_index ={}
    annotation_list = []
    for video_name in video_list:
        caption = ''
        video_path = build_video_path(base_path, video_name)
        if video_name in cc_dict and not in annotated_index:
            print 'Annotating: %s'%(video_name)
            print 'Caption: %s'%(cc_dict[video_name])
            skipped, start_frame, end_frame, ss = display_video_capture(video_path)
            if not skipped:
                annotated_index[video_name]='annotated'
                annotation_list.append((video_name+'.avi', start_frame, end_frame, caption))
                open(annotations_path, 'a').write('\t'.joint((video_name+'.avi', start_frame, end_frame, caption))
            else:
                annotated_index[video_name]='skipped'
            pickle.dump(annotated_index,open('annotatedIdx.p','wb'))

def display_capture_settings_menu():
    settings_filename = 'capsettings.p'
    #Load previous settings
    if os.path.isfile(settings_filename):
        settings = pickle.load(open(settings_filename, 'rb'))
    else:
        #Default values ['base_path', 'output_path','video_dir','movie_dir']
        settings = VASettings(base_path="/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDtranscription",\
                            output_path="/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDTranscriptionKeyFrames",\
                            movie_dir='THE_VOW',\
                            video_dir="video",\
                            cc_dict_path='/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_dict.p')
    
    #Ask for changes or leave default
    print 'Setting up the frame grabber, leave the entry empty if you would like to work with default value.'
    #BASE PATH
    inText = raw_input("Base path (%s):\n"%(settings.base_path))
    if len(inText) > 0:
        settings.base_path = inText
    #OUTPUT PATH
    inText = raw_input("Output path (%s):\n"%(settings.output_path))
    if len(inText) > 0:
        settings.output_path = inText
    #CAPTIONS DICTIONARY
    inText = raw_input("Captions dictionary (%s):\n"%(settings.cc_dict_path))
    if len(inText) > 0:
        settings = settings.cc_dict_path = inText
    #VIDEO DIR
    inText = raw_input("Path to video (%s):\n"%(settings.video_dir))
    if len(inText) > 0:
        settings = settings.video_dir = inText
    #MOVIES DIR
    inText = raw_input("Type the folder name of the movie (%s):"%(settings.movie_dir))
    if len(inText) > 0:
        settings = settings.movie_dir = inText
    
    # Save current settings
    pickle.dump(settings, open(settings_filename, 'wb'))
    
    return settings

def display_annotate_settings_menu():
    settings_filename = 'annosettings.p'
    #Load previous settings
    if os.path.isfile(settings_filename):
        settings = pickle.load(open(settings_filename, 'rb'))
    else:
        #Default values
        settings = VASettings(base_path='/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDtranscription/',\
                            video_list_path="/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/actions_video_list.txt",\
                            output_path="/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/video_action_annotations.csv",\
                            cc_dict_path='/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_dict.p')
    
    #Ask for changes or leave default
    print 'Setting up the video annotator, leave the entry empty if you would like to work with the default value.'
    #BASE PATH
    inText = raw_input("Base path (%s):\n"%(settings.base_path))
    if len(inText) > 0:
        settings.base_path = inText
    #VIDEO LIST FILE
    inText = raw_input("Video list file (%s):\n"%(settings.video_list_path))
    if len(inText) > 0:
        settings.video_list_path = inText
    #OUTPUT FILE
    inText = raw_input("Output file (%s):\n"%(settings.output_path))
    if len(inText) > 0:
        settings.output_path = inText
    #CAPTIONS DICTIONARY
    inText = raw_input("Captions dictionary (%s):\n"%(settings.cc_dict_path))
    if len(inText) > 0:
        settings = settings.cc_dict_path = inText
    
    # Save current settings
    pickle.dump(settings, open(settings_filename, 'wb'))
    
    return settings


if __name__ == '__main__': 
    '''
    Main entry point of the program
    '''
    app_mode = '0'
    while app_mode != '1' and app_mode != '2':
        app_mode = raw_input('Select the annotation mode:\n(1) Capture Frame \n(2) Annotate time\n')
        if app_mode != '1' and app_mode != '2':
            print 'Please select an option between 1 or 2.'
    
    if app_mode == '1':
        settings = display_capture_settings_menu()
        capture_movie_frames(settings.base_path, settings.output_path, settings.video_dir, settings.movie_dir, settings.cc_dict_path)
    elif app_mode == '2':
        settings = display_annotate_settings_menu()
        annotate_movie_times(settings.base_path, settings.video_list_path, settings.cc_dict_path, settings.output_path)
    
    print 'Session ended'
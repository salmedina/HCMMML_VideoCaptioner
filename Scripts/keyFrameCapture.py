#!/usr/bin/env python

import cv2
import os
import fileinput
import fnmatch
import pdb
import tty, sys, termios
import select
import pickle
from collections import deque
from collections import namedtuple
from matplotlib import pyplot as plt

Settings = namedtuple('Settings', ['base_path', 'output_path','video_dir','movie_dir'])

def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)

def getch(timeout=None):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setup_term(fd)
        try:
            rw, wl, xl = select.select([fd], [], [], timeout)
        except select.error:
            return
        if rw:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def capture_movie_frames(base_path,path1,path2,out_path):
    '''
    All the videos in the paths are shown to the user
    The player allows through keyboard input to play/pause and capture the video
    '''
    # make the output path if it does not exist
    if not os.path.isdir(os.path.join(out_path,path1)):
        os.makedirs(os.path.join(out_path,path1))
    
    #Go through all the video files in the folder
    for video_filename in os.listdir(os.path.join(base_path,path1,path2)):
        #The original videos are in .avi format
        if fnmatch.fnmatch(video_filename,'*.avi'):
            print 'Seeking frame for: %s'%(video_filename)
            #Persist until a video frame is captured
            captured_frame = False
            while not captured_frame:
                # start the video capture object
                video_paused = False
                inbuffer_index = 0
                frame_buffer = deque(maxlen=60)
                video_capture = cv2.VideoCapture(os.path.join(base_path,path1,path2,video_filename))
                ret, cur_frame = video_capture.read()
                frame_num = 1
                frame_buffer.append((frame_num, cur_frame))
                
                while ret:
                    if not video_paused:
                        if inbuffer_index < 0:   #we are reading from buffer
                            _, cur_frame = frame_buffer[inbuffer_index]
                            inbuffer_index += 1
                        else:
                            ret, cur_frame = video_capture.read()
                            frame_num += 1  #always show from frame 2
                            frame_buffer.append((frame_num, cur_frame))
                    if ret:
                        # Show the frame
                        cv2.imshow(video_filename, cur_frame)
                        
                        # Monitor keyboard input
                        key = cv2.waitKey(33) #33 [ms] to achieve ~30 FPS
                        
                        if key == 32:  # SPACE: Toggle PAUSE / PLAY
                            if video_paused:
                                video_paused = not video_paused
                        elif key == ord('n') or key == ord('N'):  # STEP BACK
                            video_paused = True
                            if len(frame_buffer) > 0 and len(frame_buffer)+inbuffer_index > 1:
                                inbuffer_index -= 1
                                _,cur_frame = frame_buffer[inbuffer_index]
                            print len(frame_buffer), inbuffer_index, frame_num+inbuffer_index
                        elif key == ord('m') or key == ord('M'):  # STEP FORWARD
                            video_paused = True
                            if inbuffer_index < -1: #we are navigating within the buffer
                                inbuffer_index += 1
                                _,cur_frame = frame_buffer[inbuffer_index]
                            else:
                                inbuffer_index = 0
                                ret, cur_frame = video_capture.read()
                                frame_num += 1  #always show from frame 2
                                frame_buffer.append((frame_num, cur_frame))
                            print len(frame_buffer), inbuffer_index, frame_num+inbuffer_index
                        elif key == ord('.'): # Store frame
                            # Capture current frame
                            outfile = video_filename[0:len(video_filename)-4] + '_%05d' %(frame_num+inbuffer_index) + '.png'
                            print "Saving frame %s"%(outfile)
                            cv2.imwrite(os.path.join(out_path,path1,outfile),cur_frame)
                            captured_frame = True
                            break
                        elif key == 27: # ESC: exit program 
                            cv2.destroyWindow(video_filename)
                            return
                        
                cv2.destroyWindow(video_filename)

def main(base_path, out_path, path2vid, movie_path):
    # Ensure output path exists
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    # Process all the clips of the movie
    capture_movie_frames(base_path,movie_path[0:len(movie_path)],path2vid,out_path)

                
if __name__ == '__main__': 
    '''
    Main entry point of the program
    '''
    settings_filename = 'settings.p'
    #Load previous settings
    if os.path.isfile(settings_filename):
        settings = pickle.load(open(settings_filename, 'rb'))
    else:
        #Default values ['base_path', 'output_path','video_dir','movie_dir']
        settings = Settings("/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDtranscription",\
                            "/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/DVDTranscriptionKeyFrames",\
                            "video",\
                            'THE_VOW')
    
    #Ask for changes or leave default
    print 'Setting up frame grabber, leave empty if you would like to work with default.'
    inText = raw_input("Base path (%s):\n"%(settings.base_path))
    if inText is not '':
        settings.base_path = inText
    inText = raw_input("Output path (%s):\n"%(settings.output_path))
    if inText is not '':
        settings.output_path = inText
    inText = raw_input("Path to video (%s):\n"%(settings.video_dir))
    if inText is not '':
        settings.video_dir = inText
    inText = raw_input("Type the folder name of the movie (%s):"%(settings.movie_dir))
    if inText is not '':
        settings.movie_dir = inText
    
    # Save current settings
    pickle.dump(settings, open(settings_filename, 'wb'))
    
    #Start program
    main(settings.base_path, settings.output_path, settings.video_dir, settings.movie_dir)
    
    print 'Session ended'
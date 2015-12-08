import cv2
import os
import fileinput
import fnmatch
import pdb
import tty, sys, termios
import select
from matplotlib import pyplot as plt

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



## funtion to recursively convert video to frames
def video2frames(base_path,path1,path2,out_path):
    # make the output path if it does not exist
    if ( not os.path.isdir(os.path.join(out_path,path1)) ):
        os.makedirs(os.path.join(out_path,path1))
        
    for file in os.listdir(os.path.join(base_path,path1,path2)):
        if fnmatch.fnmatch(file,'*.avi'):
            captureFlag = 0
            while captureFlag == 0:                
                # start the video 
                video_capture = cv2.VideoCapture(os.path.join(base_path,path1,path2,file))
                frameNum = 1
                # print
                print file

                
                while True:
                    # get frame by frame
                    ret, frame = video_capture.read()

                    #break if there are no more frames
                    if ret == False:
                        break

                    # outfile name
                    outfile = file[0:len(file)-4] + '_%05d' %(frameNum) + '.png'
                        
                    # At this point a video frame exists
                    # TODO show the image
                    
                    # fig = plt.figure()
                    plt.ion()
                    plt.imshow(frame, cmap = 'gray', interpolation = 'bicubic')
                    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
                    plt.draw()
#                   plt.show(block=False)
                    #getch()

                    # cv2.imshow("window", frame)
                    # cv2.waitKey(0)
                    character = getch()
                    if character == '.':
                        print "saved"
                        captureFlag = 1
                        plt.close()
                        break
                    frameNum += 1
                    plt.close()    

                if captureFlag == 1:
                    print os.path.join(out_path,path1[0:len(path1)],outfile)    
                    cv2.imwrite(os.path.join(out_path,path1,outfile),frame)
                    
                
                

                
if __name__ == '__main__': 
    
    ##defining the basic variables
    base_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscription"
    out_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscriptionKeyFrames"
    path2vid = "video"

    ## make the output path if it does not exist
    if ( not os.path.isdir(out_path) ):
        os.makedirs(out_path)

    ## reading stdin line by line and generating frames for the given movies
    # for line in fileinput.input():
    #     print line
    line = raw_input("Type the folder name of the movie:")
    video2frames(base_path,line[0:len(line)],path2vid,out_path)
    


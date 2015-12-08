import cv2
import os
import fileinput
import fnmatch
import pdb
import numpy as np

num_frames = []

## funtion to recursively convert video to frames
def video2frames(base_path,path1,path2,out_path):
    # make the output path if it does not exist
    if ( not os.path.isdir(os.path.join(out_path,path1)) ):
        os.makedirs(os.path.join(out_path,path1))
        
    for file in os.listdir(os.path.join(base_path,path1,path2)):
        if fnmatch.fnmatch(file,'*.avi'):
            # make the output path if it does not exist
            if ( not os.path.isdir(os.path.join(out_path,path1,file[0:len(file)-4])) ):
                os.makedirs(os.path.join(out_path,path1,file[0:len(file)-4]))
            # start the video 
            video_capture = cv2.VideoCapture(os.path.join(base_path,path1,path2,file))
            count = 0
            # print
           # print file
            while True:
                # get frame by frame
                ret, frame = video_capture.read()

                #break if there are no more frames
                if ret == False:
                    num_frames.append(count)
                    print count
                    break
                count= count + 1



#defining the basic variables
base_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscription"
out_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscriptionFrames"
path2vid = "video"

# make the output path if it does not exist
if ( not os.path.isdir(out_path) ):
    os.makedirs(out_path)

# reading stdin line by line and generating frames for the given movies
for line in fileinput.input():
    #print line
    video2frames(base_path,line[0:len(line)-1],path2vid,out_path)

pdb.set_trace()    
num_frames = np.array(num_frames)
print num_frames.sum()
num_time = num_frames/24
print num_time.mean()
print num_time.var()

pdb.set_trace()
#pickle.dump( dictionary, open( "frames.p", "wb" ) )
pdb.set_trace()    
    


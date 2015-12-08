import cv2
import os
import fileinput
import fnmatch
import pdb

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
            count = 24
            num = 1
            # print
            print file
            while True:
                # get frame by frame
                ret, frame = video_capture.read()

                #break if there are no more frames
                if ret == False:
                    break

                if count == 24 :
                    outfile = os.path.join(file[0:len(file)-4], file[0:len(file)-4] + '_%05d' %(num) + '.png')
                    #print os.path.join(out_path,path1[0:len(path1)-4],outfile)
                    cv2.imwrite(os.path.join(out_path,path1,outfile),frame)
                    num = num + 1
                    count = 0
                count= count + 1

                

if __name__ == '__main__': 
    
    ##defining the basic variables
    base_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscription"
    out_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscriptionFrames"
    path2vid = "video"

    ## make the output path if it does not exist
    if ( not os.path.isdir(out_path) ):
        os.makedirs(out_path)

    ## reading stdin line by line and generating frames for the given movies
    for line in fileinput.input():
        print line
        video2frames(base_path,line[0:len(line)-1],path2vid,out_path)
    


import cv2
import os
import fileinput
import fnmatch
import pdb
from dominant_color import get_dominant_color

def recursive_dive(base_path,dictionary):
    listDir = os.listdir(base_path)
    for filename in listDir:
        if os.path.isdir(os.path.join(base_path,filename)):
            recursive_dive(os.path.join(base_path,filename),dictionary)
        else :
            if fnmatch.fnmatch(filename,'*.png'):
                image = cv2.imread(os.path.join(base_path,filename))
                dictionary.update({filename:get_dominant_color(image)})
                print filename
                
def main():                    
    #defining the basic variables
    base_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscriptionFrames"
    out_path = "/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/"
    dictionary = {}
    recursive_dive(base_path,dictionary)
    pickle.dump( dictionary, open( "dominant_colour.p", "wb" ) )
    pdb.set_trace()
if __name__ == '__main__':
    main()


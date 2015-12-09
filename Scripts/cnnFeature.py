import os
import pickle as pk
import subprocess
import pdb
import numpy as np


def extract_features(imagePath):
    overfeat_path = '/home/chahuja/Downloads/softwares/OverFeat/bin/linux_64/overfeat'
    output = subprocess.Popen([overfeat_path, '-f', imagePath], stdout=subprocess.PIPE).communicate()[0]
    output = output.split()
    lt = int(output.pop(0))
    ht = int(output.pop(0))
    wt = int(output.pop(0))
    feature = [float(output[i]) for i in range(len(output))]
    #feature = np.array(feature)
    return feature
#pdb.set_trace()

if __name__ == '__main__':
    basePath  = '/media/chahuja/DATAPART1/my-data/gdrive/SEM1/Multimodal/project/HCMMML_VideoCaptioner/Data/'
    imageNameList = os.listdir(basePath)
    ## First Image's feature extraction to determine the shape of the features
    feature = extract_features(os.path.join(basePath,imageNameList.pop(0)))
    ## Create an Empty feature Matrix
    featureMatrix = np.zeros(shape = (len(imageNameList)+1,len(feature)))
    ## Add the first image to featureMatrix
    featureMatrix[0] = feature

    count = 1
    print count 
    for imagePath in imageNameList:
        imagePath = os.path.join(basePath,imagePath)
        feature = extract_features(imagePath)
        featureMatrix[count] = feature
        count += 1
        print count

    pdb.set_trace()

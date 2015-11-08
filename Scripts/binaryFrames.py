import os
import numpy as np
import cv2
import cPickle as pickle
from skimage import io

videoFilePath = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/TestGround/'
dumpFile = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/TestGround/THE_BOUNTY_HUNTER_DVS589.np'

index = 0
frames = []
for item in os.listdir(videoFilePath):
    fullItemPath = os.path.join(videoFilePath, item)
    if os.path.isfile(fullItemPath) and item.endswith('.jpg'):
        frame = io.imread(fullItemPath)
        frames.append(np.array(frame, dtype=np.float64) / 255)

np.save(open(dumpFile, 'wb'), frames)
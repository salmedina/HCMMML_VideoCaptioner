import os
import numpy as np
import cv2
import cPickle as pickle

videoFile = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/TestGround/THE_BOUNTY_HUNTER_DVS589.avi'
dumpFile = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/TestGround/THE_BOUNTY_HUNTER_DVS589.pkl'
vidcap = cv2.VideoCapture(videoFile)
success,frame = vidcap.read()

index = 0
frames = []
while success:
    frames.append(np.array(frame, dtype=np.float64) / 255)
    success,frame = vidcap.read()

pickle.dump(frames, open(dumpFile, 'wb'))
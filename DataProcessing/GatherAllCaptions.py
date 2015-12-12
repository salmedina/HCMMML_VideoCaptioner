import os
import glob
import cPickle as pickle
from os.path import join

all_srt_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files/all_srt'
save_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/AllMovies/all_captions.txt'

all_captions = []
for srt_file in glob.glob(join(all_srt_path,'*.srt')):
    movie_name = os.path.splitext(os.path.basename(srt_file))[0]
    all_lines = open(join(all_srt_path, srt_file),'r').readlines()
    for i in range(0,len(all_lines),4):
        all_captions.append(all_lines[i+2].strip())
        
save_file = open(save_filename, 'wb')
save_file.write('\n'.join(all_captions))
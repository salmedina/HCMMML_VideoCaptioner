import os
import glob
import cPickle as pickle
from os.path import join

all_srt_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files/all_srt'
save_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/all_captions_dict.p'

captions_dict = {}
for srt_file in glob.glob(join(all_srt_path,'*.srt')):
    movie_name = os.path.splitext(os.path.basename(srt_file))[0]
    all_lines = open(join(all_srt_path, srt_file),'r').readlines()
    for i in range(0,len(all_lines),4):
        captions_dict[all_lines[i].strip()]=all_lines[i+2].strip()
        
pickle.dump(captions_dict,open(save_filename, 'wb'))
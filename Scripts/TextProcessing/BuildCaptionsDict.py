#!/usr/bin/env python

import os
import glob
import cPickle as pickle
from os.path import join
import NLPAnalysis as nlpa

all_srt_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files/all_srt'
dict_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_dict.p'
inv_dict_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_inv_dict.p'
verbs_dict_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_verbs_dict.p'

captions_dict = {}
captions_inv_dict = {}
verbs_dict = {}

for srt_file in glob.glob(join(all_srt_path,'*.srt')):
    movie_name = os.path.splitext(os.path.basename(srt_file))[0]
    all_lines = open(join(all_srt_path, srt_file),'r').readlines()
    for i in range(0,len(all_lines),4):
        file_name = all_lines[i].strip()
        caption = all_lines[i+2].strip()

        #Captions dict
        captions_dict[file_name]=caption
        #Inverted dict based on captions
        captions_inv_dict[caption]=file_name
        #Inverted dict based on verbs
        caption_verbs = nlpa.extract_lemmatized_verbs(caption.decode('utf8'))
        for verb in caption_verbs:
            if verb not in verbs_dict:
                verbs_dict[verb] = [(file_name, caption)]
            else:
                verbs_dict[verb].append((file_name, caption))
        
pickle.dump(captions_dict,open(dict_filename, 'wb'))
pickle.dump(captions_inv_dict,open(inv_dict_filename, 'wb'))
pickle.dump(verbs_dict, open(verbs_dict_filename, 'wb'))
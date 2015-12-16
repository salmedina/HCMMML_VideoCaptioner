from __future__ import division
import os
import re
import re
import sys
import json
import cPickle as pickle
import NLPAnalysis as nlpa


def get_videoname(action_img):
    name_pattern = re.compile('(.*_DVS.*)_\d+.png')
    videoname = name_pattern.search(action_img).group(1)
    return videoname

#input file
nt_results_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Results/test-captions-3.csv'
captions_dict_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_dict.p'
#Constants
SEPARATOR = ':'

if not os.path.isfile(nt_results_path):
    print 'Invalid NeuralTalk results file'
    sys.exit(-1)

captions_dict = pickle.load(open(captions_dict_path))
generated_captions_list = open(nt_results_path, 'r').readlines()

tp = 0
for gc_item in generated_captions_list:
    frame_filename, generated_caption = gc_item.split(SEPARATOR)
    frame_filename = frame_filename.strip()
    generated_caption = generated_caption.strip()
    video_filename = get_videoname(frame_filename)
    if not video_filename in captions_dict:
        print 'Video was not found in dictionary:\n%s'%(video_filename)
        continue
    
    original_caption = captions_dict[video_filename]
    generated_verbs = nlpa.extract_lemmatized_verbs(generated_caption)
    original_caption = nlpa.remove_invalid_unicode(original_caption)  #clean-up caption
    original_verbs = set(nlpa.extract_lemmatized_verbs(original_caption))
    
    for gverb in generated_verbs:
        if gverb in original_verbs:
            tp += 1
            break

tp_rate = tp/len(generated_captions_list)
print 'TP:                 %d'%tp
print 'Total captions:     %d'%len(generated_captions_list)
print 'True positive rate: %04f'%(tp_rate)
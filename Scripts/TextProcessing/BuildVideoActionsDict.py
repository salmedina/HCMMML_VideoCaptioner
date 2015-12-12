import os
import cPickle as pickle

verbs_dict_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_verbs_dict.p'
videoaction_dict_filename = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_video_action_dict.p'

verbs_dict = pickle.load(open(verbs_dict_filename))

video_action_dict = {}
for verb in verbs_dict:
    dict_entry = verbs_dict[verb]
    video_list = zip(*dict_entry)[0]
    for video in video_list:
        if video not in video_action_dict:
            video_action_dict[video]=[verb]
        else:
            video_action_dict[video].append(verb)
    
    
pickle.dump(video_action_dict, open(videoaction_dict_filename, 'wb'))
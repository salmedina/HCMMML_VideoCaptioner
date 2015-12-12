import os
import sys
import cPickle as pickle

verb_dict_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/all_captions_verbs_dict.p'
actions_list_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/VideoAnnotation/actions_of_interest.txt'
output_dir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/VideoAnnotation'

if not os.path.isfile(verb_dict_path):
   print 'Invalid verbs dict file'
   sys.exit(-1)

if not os.path.isdir(output_dir):
   print 'Invalid output directory'
   sys.exit(-1)
   
if not os.path.isfile(actions_list_path):
   print 'Invalid actions list file'
   sys.exit(-1)

#Load necessary variables
verb_dict = pickle.load(open(verb_dict_path))
action_list = open(actions_list_path).readlines()
action_list = map(lambda x: x.strip(), action_list)
#build a list of videos per action
for action in action_list:
   savefile_path = os.path.join(output_dir, '%s.txt'%(action))
   if action in verb_dict:
      entry_list = verb_dict[action]
      videos_with_action = zip(*entry_list)[0]
      open(savefile_path, 'w').write('\n'.join(videos_with_action))
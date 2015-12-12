import os
import glob

num_list = []
for actionFile in os.listdir('/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Repository/DataProcessing/VideoAnnotation/'):
    num_list.append( ('%05d'%(len(open(actionFile).readlines())), actionFile) )
    
num_list.sort()

for item in num_list:
    print item
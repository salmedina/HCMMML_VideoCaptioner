import os
import codecs
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag

def get_files_with_keyword(path, keyword):
    files_with_someone = []
    
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            lines = open(os.path.join(path, item), 'r').readlines()
            for i in range(2, len(lines), 4):
                if keyword in lines[i]:
                    files_with_someone.append(lines[i-2])
    return files_with_someone

def get_verbs(path):
    found_verbs = []
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            lines = codecs.open(os.path.join(path, item), 'r', encoding='utf-8').readlines()
            for i in range(2, len(lines), 4):
                if 'SOMEONE' in lines[i]:
                    tokens = word_tokenize(lines[i])
                    tagged_tokens = pos_tag(tokens)
                    for item in tagged_tokens:
                        if 'VB' in item[1]:
                            found_verbs.append(item[0])
    return found_verbs

def generate_someone_lists():
    srt_paths = ['/Users/zal/CMU/Fall2015/HCMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files/train_srt',\
    '/Users/zal/CMU/Fall2015/HCMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files/valid_srt',\
    '/Users/zal/CMU/Fall2015/HCMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files/test_srt']
    output_filename = ['TrainList_Someone.txt', 'ValidList_Someone.txt', 'TestList_Someone.txt']
    
    for srt_path, output_filename in zip(srt_paths, output_filename):
        files_with_someone = get_files_with_keyword(srt_path, 'SOMEONE')
        open(output_filename, 'w').writelines(files_with_someone)

def generate_verbs_list():
    verbs_list = get_verbs(srt_paths[0])
    codecs.open('TrainVerbsList.txt', 'w', encoding='utf-8').write('\n'.join(verbs_list))
    
def plot_verbs_wordcloud():
    
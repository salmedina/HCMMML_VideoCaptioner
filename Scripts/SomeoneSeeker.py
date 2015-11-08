import os
import codecs
from nltk import word_tokenize, pos_tag


def get_files_with_keyword(path, keyword):
    files_with_keyword = []
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            lines = open(os.path.join(path, item), 'r').readlines()
            for i in range(2, len(lines), 4):
                if keyword in lines[i]:
                    files_with_keyword.append(lines[i-2])
    return files_with_keyword

def generate_someone_lists():
    dataset_path = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/'
    srt_paths = ['M-VAD/srt_files/train_srt', 'M-VAD/srt_files/valid_srt','M-VAD/srt_files/test_srt']
    
    for srt_path, output_filename in zip(srt_paths, output_filename):
        files_with_someone = get_files_with_keyword(srt_path, 'SOMEONE')
        open(output_filename, 'w').write('\n'.join(files_with_someone))

if __name__ == '__main__':
    generate_someone_lists()
import os
import re
from nltk.stem.wordnet import WordNetLemmatizer
import multiprocessing as mp

def flatten_list(inList):
    return [item for sublist in inList for item in sublist]

def extract_captions(captionsFileList):
    captions = []
    for captionsFile in captionsFileList:
        lines = open(captionsFile).readlines()
        for i in range(2, len(lines), 4):
            if keyword in lines[i]:
                captions.append(lines[i])
    return captions

def extract_pos_of_sentence(sentence):
    sentencesTokens = nltk.word_tokenize(sentence)  # Converts into list of words
    posTokens = nltk.pos_tag(sentencesTokens)       # Return list of tuples (word, POS)
    return posTokens

def get_verbs_from_sentence(posSentence):
    verbs = []
    return [word for word,pos in posSentence if re.match(r'\VB.*',pos)]

def lemmatize_verb(verb):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(verb, 'v')

def mp_lemmatize_verbs(verbs):
    return mp_process_iterable(lemmatize_verb, verbs)

def mp_get_verbs(posSentences):
    return mp_process_iterable(get_verbs_from_sentence, posSentences)
    
def mp_extract_pos(sentences):
    return mp_process_iterable(extract_pos_of_sentence, sentences)

def mp_lemmatize_verbs(verbs):
    return mp_process_iterable(lemmatize_verb, verbs)

def mp_process_iterable(func, iterable):
    numThreads = mp.cpu_count()-1
    pool = mp.Pool(numThreads)
    
    res = pool.map(func, iterable)
    
    pool.close()
    pool.join()
    
    return res

def main():
    captionsDir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files'
    romantic_list_filepath = '../DataProcessing/romantic_movies.txt'
    romantic_list_someone_filepath = ''
    romantic_someone_captions_filepath = ''
    romantic_someone_pos_captions_filepath = ''
    romantic_someone_verbs_filepath = ''
    romantic_someone_lemmatized_verbs_filepath = ''
    pass

if __name__ =='__main__':
    main()
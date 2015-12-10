import os
import re
import nltk
import collections
from nltk.stem.wordnet import WordNetLemmatizer
import multiprocessing as mp
import cPickle as pickle


MovieClip = collections.namedtuple('MovieClip', 'filename caption pos verbs lemma_verbs')

def flatten_list(inList):
    return [item for sublist in inList for item in sublist]

def add_to_count_dict(dictionary, item):
    '''Adds a count of 1 to the entry item in a counting dictionary'''
    if item not in dictionary:
        dictionary[item] = 1
    else:
        dictionary[item] += 1
    return dictionary

def pretty_print_count_dict(dictionary):
    dictTuples = []
    for item in dictionary:
        dictTuples.append((dictionary[item], item))
    
    dictTuples.sort(key = lambda x: x[0], reverse=True)
    
    printLines = []
    for count, verb in dictTuples:
        printLines.append('%d   %s'%(count, verb))
    
    print ''.join(printLines)

def extract_pos_of_sentence(sentence):
    sentencesTokens = nltk.word_tokenize(sentence)  # Converts into list of words
    posTokens = nltk.pos_tag(sentencesTokens)       # Return list of tuples (word, POS)
    return posTokens

def get_verbs_from_sentence(posSentence):
    verbs = []
    return [word for word,pos in posSentence if re.match(r'VB.*', pos)]

def lemmatize_verb(verbs):
    lemmatizer = WordNetLemmatizer()
    return map(lambda x:lemmatizer.lemmatize(x, 'v'),verbs)

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

def load_filelines_as_list(fileName):
    fileLines = []
    if os.path.isfile(fileName):
        fileLines = open(fileName, 'r').readlines()
    return fileLines

def extract_caption_sentences(captionsSRTFileName, saveFileName):
    srtLines = open(captionsSRTFileName,'r').readlines()
    captionSentences = []
    #SRT Files are formed by lines as follows:
    #clip name
    #time in movie
    #caption
    #blank line
    #The thing is that the first caption is not preceded by a blank line
    #Therefore we calculate the captions lines as follows:
    captionSentences = [srtLines[i] for i in range(2,len(srtLines),4)]
    
    open(saveFileName,'w').write(''.join(captionSentences))
    return captionSentences

def get_lemmatized_verbs():
    captionsDir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files'
    romantic_list_filepath = '../DataProcessing/romantic_movies.txt'
    captionsSRTFileName = '../DataProcessing/romantic_captions.srt'
    romanticCaptionSentencesFileName = '../DataProcessing/romantic_caption_sentences.txt'
    captionsPOSFileName = '../DataProcessing/romantic_caption_pos.pkl'
    captionsPOSVerbsFileName = '../DataProcessing/romantic_caption_pos_verbs.pkl'
    captionsLemmaVerbsFileName = '../DataProcessing/romantic_lemmatized_verbs.txt'
    
    sentences = load_filelines_as_list(romanticCaptionSentencesFileName)
    sentences = map(lambda x:x.decode('utf8'), sentences)
    posSentences = mp_extract_pos(sentences)
    pickle.dump(posSentences, open(captionsPOSFileName, 'wb'))
    
    verbs = mp_get_verbs(posSentences)
    pickle.dump(posSentences, open(captionsPOSVerbsFileName, 'wb'))
    
    lemmatizedVerbs = mp_lemmatize_verbs(verbs)
    lemmatizedVerbs = flatten_list(lemmatizedVerbs)
    open(captionsLemmaVerbsFileName,'w').write('\n'.join(lemmatizedVerbs).encode('utf8'))

def analyze_lemmatized_verbs():
    captionsLemmaVerbsFileName = '../DataProcessing/romantic_lemmatized_verbs.txt'
    lemmVerbs = load_filelines_as_list(captionsLemmaVerbsFileName)
    countDict = {}
    for verb in lemmVerbs:
        add_to_count_dict(countDict, verb)
    
    pretty_print_count_dict(countDict)
    

if __name__ =='__main__':
    analyze_lemmatized_verbs()
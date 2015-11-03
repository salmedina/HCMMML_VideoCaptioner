import os
import urllib2
import json

def get_movie_list(movieFile):
    res = []
    if os.path.isfile(movieFile):
        res = open(movieFile, 'r').readlines()
    return res
    
def get_movie_info(title):
    request_title = title.lower().replace(' ', '+')
    request_title = request_title.replace('_', '+')
    opendb_request = 'http://www.omdbapi.com/?t=%s&y=&plot=full&r=json'%(request_title)
    jsonRes = json.load(urllib2.urlopen(opendb_request))
    return jsonRes

def analyze_movie_genre(genreFile):
    pass

def main():
    movieFile = '/Users/zal/CMU/Fall2015/HCMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/MovieList.txt'
    movieList = get_movie_list(movieFile)
    for movieTitle in movieList:
        movieInfo = get_movie_info(movieTitle.strip())
        if 'Genre' in movieInfo:
            print movieInfo['Title'] + '\t'+ movieInfo['Genre']

if __name__ == '__main__':
    main()
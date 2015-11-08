import os
import urllib2
import json
import matplotlib.pyplot as plt

def get_basename_no_ext(path):
    return os.path.splitext(os.path.basename(path))[0]

def add_to_count_dict(dictionary, item):
    '''Adds a count of 1 to the entry item in a counting dictionary'''
    if item not in dictionary:
        dictionary[item] = 1
    else:
        dictionary[item] += 1
    return dictionary

def get_movie_list(movieFile):
    '''Reads a movie list file and returns the list of titles'''
    res = []
    if os.path.isfile(movieFile):
        res = open(movieFile, 'r').readlines()
    return res

def query_movie_info_from_omdb(title):
    '''Requests info from open movie database and returns the JSON answer'''
    request_title = title.lower().replace(' ', '+')
    request_title = request_title.replace('_', '+')
    opendb_request = 'http://www.omdbapi.com/?t=%s&y=&plot=full&r=json'%(request_title)
    jsonRes = json.load(urllib2.urlopen(opendb_request))
    return jsonRes

def build_movie_genre_file(movieListFileName, saveFileName):
    '''Creates a list of files with its genres obtained from the open movie database'''
    movieList = get_movie_list(movieListFileName)
    
    movieGenreLines =[]
    for movieTitle in movieList:
        movieInfo = query_movie_info_from_omdb(movieTitle.strip())
        if 'Genre' in movieInfo:
            print  movieInfo['Title'] + '\t'+ movieInfo['Genre']
            movieGenreLines.append(movieInfo['Title'] + '\t'+ movieInfo['Genre'])
        else:
            movieGenreLines.append(movieTitle.strip() + '\tN/A')
    
    saveFile = open(saveFileName, 'wb')
    saveFile.write('\n'.join(movieGenreLines))
    saveFile.close()
    return movieGenreLines

def load_movie_info(movieInfoFile):
    '''Returns a list of a tuple (titleStr, listOfGenres)'''
    movieList = []
    if os.path.isfile(movieInfoFile):
        genreLines = open(movieInfoFile, 'r').readlines()
        for line in genreLines:
            movieTitle, genres = line.split('\t')
            movieGenres = genres.strip().split(',')
            movieGenres = map(lambda x:x.strip(), movieGenres)
            movieList.append((movieTitle, movieGenres))
    return movieList
    
def print_genre_sets(movieInfoFile):
    '''Prints out the sets of mixed genres and its count'''
    genreDict = {}
    
    for title, genres in load_movie_info(movieInfoFile):
        genreDict = add_to_count_dict(genreDict, ','.join(genres))
            
        genreCountLines = []
        for item in genreDict:
            print '%d\t%s'%(genreDict[item], item)
            genreCountLines.append('%d\t%s'%(genreDict[item], item))
    
    return genreDict

def plot_genre_histogram(genreFileName):
    genreList = []
    for title, genres in load_movie_info(movieInfoFile):
        genreList.extend(genres)
    
    countDict = {}
    for item in genreList:
        countDict = add_to_count_dict(countDict, item)
    
    count = []
    genre = []
    for item in countDict:
        count.append(countDict[item])
        genre.append(item)
    
    plt.hist(count, bins = len(count))
    plt.show()
    
def get_genres_that_go_with(targetGenre, movieInfoFile):
    '''Prints a list of genres that were found in the movies alongside the target genre'''
    withGenreDict = {}
    
    for title, genres in load_movie_info(movieInfoFile):
        if targetGenre in genres:
            for genre in [x for x in genres if x != targetGenre]:
                withGenreDict = add_to_count_dict(withGenreDict, genre)

    for item in withGenreDict:
        print '%d   %s'%(withGenreDict[item], item)
    
    return withGenreDict

def get_movies_by_genre(targetGenre, movieInfoFile):
    '''Gets a list of movies according to the target genre'''
    movieList = []
   
    for title, genres in load_movie_info(movieInfoFile):
        if targetGenre in genres:
            movieList.append(title)
    
    return movieList

def build_movie_captions_by_genre(targetGenre, captionsDir, saveFileName):
    '''Saves into a file all the srt file paths corresponding to that genre'''
    movieGenreFileName = '../DataProcessing/movie_genre.txt'
    romanticCaptionFileName = '../DataProcessing/romantic_caption_list.txt'
    
    #Get list of romantic movies
    target_movies = get_movies_by_genre(targetGenre, movieGenreFileName)
    #Process to be as Motreal DSV names
    target_movies = map(lambda x: x.replace(' ', '_'), target_movies)
    target_movies = map(lambda x: x.replace('-', '_'), target_movies)
    target_movies = map(lambda x: x.upper(), target_movies)
    #Get list of srts for the target genre
    srt_subdirs = ['test_srt','train_srt','valid_srt']
    
    captionFileList = []
    for subdir in srt_subdirs:
        fullCaptionSubdir = os.path.join(captionsDir, subdir)
        for item in os.listdir(fullCaptionSubdir):
            itemFullPath = os.path.join(fullCaptionSubdir, item)
            if os.path.isfile(itemFullPath) and get_basename_no_ext(itemFullPath) in target_movies:
                captionFileList.append(os.path.join(subdir, item))
    
    open(saveFileName, 'wb').write('\n'.join(captionFileList))
    
def gather_all_captions(srtFileNames, saveFileName):
    saveLines = []
    for srtFile in srtFileNames:
        saveLines.extend(open(srtFile,'r').readlines())
    
    open(saveFileName,'w').write(''.join(saveLines))

def main_analysis():
    movieListFileName = '../DataProcessing/movie_list.txt'
    movieGenreFileName = '../DataProcessing/movie_genre.txt'
    
    print 'Building movie genre file'
    build_movie_genre_file(movieListFileName, movieGenreFileName)
    print ''
    print 'Total movies:  %d'%(len(get_movie_list(movieGenreFileName)))
    print ''
    print 'Genres that go with Romance:'
    print get_genres_that_go_with('Romance', movieGenreFileName)
    print ''
    print 'Romantic movies'
    romantic_list = get_movies_by_genre('Romance',movieGenreFileName)
    print 'Count:   %d'%(len(romantic_list))
    print '\n'.join(romantic_list)
    
def main_caption():
    movieGenreFileName = '../DataProcessing/movie_genre.txt'
    captionsDir = '/Users/zal/CMU/Fall2015/HCMMML/FinalProject/Dataset/MontrealVideoAnnotationDataset/M-VAD/srt_files'
    romanticCCFileListFileName = '../DataProcessing/romantic_caption_filelist.txt'
    allRomanticSRTFileName = '../DataProcessing/romantic_captions.srt'
    
    build_movie_captions_by_genre('Romance', captionsDir, romanticCCFileListFileName)
    allRomanticSRTs = map(lambda x: os.path.join(captionsDir, x), open(romanticCCFileListFileName,'r').readlines())
    allRomanticSRTs = [f.strip() for f in allRomanticSRTs] #Clean up the lines
    gather_all_captions(allRomanticSRTs, allRomanticSRTFileName)
    

if __name__ == '__main__':
    #main_analysis()
    main_caption()
from __future__ import division

def get_frames_of_interest(video_len, sample_size):
    if video_len < sample_size:
        return range(1,video_len,1)
    
    skip_size = int(round(video_len / sample_size))
    padding = int((video_len%sample_size) / 2)
    start_point = padding
    end_point = video_len - padding
    
    return range(start_point+1, end_point, skip_size)

#Function test

lengths = [7, 16, 31, 46, 61, 76, 91, 145]

for length in lengths:
    r = get_frames_of_interest(length, 15)
    print len(r)
    print r
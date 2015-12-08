from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2
import pdb


def get_dominant_color(image):
   # pdb.set_trace()
    # load the image and grab its width and height
    (h, w) = image.shape[:2]
    
    # convert the image from the RGB color space to the L*a*b*
    # In the L*a*b* color space the euclidean distance implies
    # perceptual meaning as in RGB it does not
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # reshape image for k-means
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    
    # Do K-means in minibatch as it is faster given that it works
    # on a subsample of the points and has similar results
    clt = MiniBatchKMeans(n_clusters = 1)
    labels = clt.fit_predict(image)
    quant = clt.cluster_centers_.astype("uint8")[labels]
    quant = quant.reshape((h, w, 3))
    
    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)
    return quant[0][0]
    
    
def main():
    sampleImage = '/media/chahuja/DATAPART1/my-data/local/MontrealVideoAnnotationDataset/DVDtranscriptionFrames/40_YEAR_OLD_VIRGIN/40_YEAR_OLD_VIRGIN_DVS100/40_YEAR_OLD_VIRGIN_DVS100_00001.png'
    image = cv2.imread(sampleImage)
    #print image
    print get_dominant_color(image)
    
if __name__ == '__main__':
    main()

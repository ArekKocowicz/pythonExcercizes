import numpy as np
import matplotlib.pyplot as plt
import cv2

def imageSummarizeRows(inputImage):
    (inputHeight, inputWidth, inputColorChannels)=inputImage.shape  #store input image size
    print(inputImage.shape)
    inputImageMono=inputImage.sum(2)                                #convert from RGB to monochrome
    inputImageMono[inputImageMono<(3*255)]=0                        #truncate, all pixel not fully white will be 0
    inputImageMono[inputImageMono>0]=1                              #truncate, all pixels fully white will be 1

    #plt.imshow(inputImageMono)
    #plt.grid()
    #plt.show()
    #cv2.waitKey(0)

    rowSum=inputImageMono.sum(1)                                    #number of fully white pixels in each row of input image
    rowSumSigned=rowSum.astype(int)                                 #change to int because later convolution with signed numbers needed
    rowSumSigned[rowSumSigned<inputWidth]=-1                        #-1 in rows which contained colors other than white
    rowSumSigned[rowSumSigned>0]=1                                  # 1 in rows which contained only white pixels
    return rowSumSigned

def imageFindTextRows(rowSumSigned, textHeight):
    #table with measurements/text is 10 pixels tall. There is always full white row below and above the text. Now search for 10 time -1 in the rowSumSigned
    patternHeight=textHeight+2                                      #how tall is the area suspected to be a text
    pattern=-1*np.ones(patternHeight)                               #this is pattern for convolution, it has (patternHeight-2) times -1 
    pattern[0]=1                                                    #and 1 at the begining and at the end
    pattern[patternHeight-1]=1
    print(pattern)

    myConv=np.convolve(rowSumSigned,pattern)                        #
    convMaxima=np.where(myConv==patternHeight)[0]                   #ndarray of found patterns

    print(convMaxima)
    return convMaxima




inputImage = cv2.imread("sw20.png")                             #read in the image
(inputHeight, inputWidth, inputColorChannels)=inputImage.shape  #store input image size
rowSumSigned=imageSummarizeRows(inputImage)
textHeight=11                                                   #expected text height
convMaxima=imageFindTextRows(rowSumSigned,textHeight)
(numberOfMaxima,)=convMaxima.shape


for i in range(numberOfMaxima):
    print(convMaxima[i])
    xtop=round(convMaxima[i]-textHeight)
    xbot=round(convMaxima[i])
    localImage=inputImage[xtop:xbot ,0:inputWidth]
    cv2.imshow("localImage",localImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

plt.plot(myConv, "r.")
plt.show()

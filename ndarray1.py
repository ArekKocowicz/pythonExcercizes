import numpy as np
import matplotlib.pyplot as plt
import cv2

inputImage = cv2.imread("sw20.png")                             #read in the image
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

plt.plot(rowSumSigned, "b.") 
plt.grid()
plt.show()

#table with measurements/text is 10 pixels tall. There is always full white row below and above the text. Now search for 10 time -1 in the rowSumSigned

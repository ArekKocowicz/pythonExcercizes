import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract
import re

def imageSummarize(inputImage, axis):
    (inputHeight, inputWidth, inputColorChannels)=inputImage.shape  #store input image size
    inputImageMono=inputImage.sum(2)                                #convert from RGB to monochrome
    inputImageMono[inputImageMono<(3*255)]=0                        #truncate, all pixel not fully white will be 0
    inputImageMono[inputImageMono>0]=1                              #truncate, all pixels fully white will be 1

    rowSum=inputImageMono.sum(axis)                                    #number of fully white pixels in each row of input image
    rowSumSigned=rowSum.astype(int)                                 #change to int because later convolution with signed numbers needed
    rowSumSigned[rowSumSigned<inputWidth]=-1                        #-1 in rows which contained colors other than white
    rowSumSigned[rowSumSigned>0]=1                                  # 1 in rows which contained only white pixels
    return rowSumSigned

#imgAxisSum takes an image and
#axis = 1 for rows
#axis = 0 for columns
#and returns a vector ( one dimension ) containing only
#-1 if there was only black
# 0 if there were different colors
# 1 if there was only white

def imgAxisSum(inputImage, axis):
    (imgHeigh, imgWidth, imgDepth)=inputImage.shape                     #store image height and width
    imgGray=cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)                #convert to grayscale
    imgGrayInv=255-imgGray                                              #invert grayscale
    axisSum=imgGray.sum(axis)                                           #calculate sum of each row or column in the image
    axisSumInv=imgGrayInv.sum(axis)
    fullBlack=np.zeros(axisSum.shape, int)
    fullWhite=np.zeros(axisSum.shape, int)
    fullBlack[axisSum==0]=1
    fullWhite[axisSumInv==0]=1
    #plt.plot(fullWhite, label="fullWhite")
    #plt.plot(fullBlack, label="fullBlack")
    #plt.legend()
    #plt.show()
    return(fullWhite, fullBlack)


def imageFindTextRows(rowSumSigned, textHeight):
    #table with measurements/text is 10 pixels tall. There is always full white row below and above the text. Now search for 10 time -1 in the rowSumSigned
    patternHeight=textHeight+2                                      #how tall is the area suspected to be a text
    pattern=-1*np.ones(patternHeight)                               #this is pattern for convolution, it has (patternHeight-2) times -1 
    pattern[0]=1                                                    #and 1 at the begining and at the end
    pattern[patternHeight-1]=1
    #print(pattern)
    myConv=np.convolve(rowSumSigned,pattern)                        #convolve pattern with rowSumSigned
    convMaxima=np.where(myConv==patternHeight)[0]                   #find only ideal matches
    print(convMaxima)
    return convMaxima.tolist()                                      #return indexes as a list

def imageCropRows(rowSumSigned, inputImage, textHeight):
    convMaxima=[]                                                   #list for indexes of convolution maximums
    croppedImages=[]                                                #list for cropped rows 
    convMaxima=imageFindTextRows(rowSumSigned,textHeight)           
    numberOfMaxima=len(convMaxima)
    for i in range(numberOfMaxima):
        xtop=round(convMaxima[i]-textHeight-1)
        xbot=round(convMaxima[i]+1)
        croppedImages.append(inputImage[xtop:xbot ,0:inputWidth])
        print("appending")
    return croppedImages


inputFileName="./png/input/sw21"
inputImage = cv2.imread(inputFileName+".png")                                 #read in the image
imgAxisSum(inputImage,1)
(inputHeight, inputWidth, inputColorChannels)=inputImage.shape      #store input image size
rowSumSigned=imageSummarize(inputImage, 1)                         #summarize row = try to predict where is text in input image
croppedImages2=imageCropRows(rowSumSigned, inputImage, 10)          #crop rows with text into separate images
croppedImages2.extend(imageCropRows(rowSumSigned, inputImage, 11))  #crop rows with text into separate images

kernel = np.ones((5, 5), np.uint8)                                  #kernel for dilation

report=""                                                           

for i in range(len(croppedImages2)):
    imgRow=croppedImages2[i]
    imgRowShape=imgRow.shape
    imgRowHeight=imgRowShape[0]
    print(f"imgRowHeight = {imgRowHeight}")
    outputFileName=inputFileName+"_"+str(i)+".png"
    cv2.imwrite(outputFileName,imgRow)

    erosion_size=7
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (2 * erosion_size + 1, 2 * erosion_size + 1),(erosion_size, erosion_size))
    img_erode = cv2.erode(imgRow, element)

    (fullWhite,fullBlack)=imgAxisSum(img_erode,0)
    mydiff=np.diff(fullWhite) 
    
    #-1 in mydiff means, that this is begin of the text, 1 means that this is end
    #if first non zero value i 1, than begining is at the pixel 0 
    ends=np.where(mydiff==1)[0]
    starts=np.where(mydiff==-1)[0]
    ends_l=ends.tolist()
    starts_l=starts.tolist()
    if len(ends_l)>len(starts_l):                                   #if more ends than begins
        starts_l.insert(0,0)
    print(starts_l)
    print(ends_l)
    for k in range(len(starts_l)):
        outputFileName=inputFileName+"_"+str(i)+"_"+str(k)+".png"
        imgTextField=imgRow[0:imgRowHeight,starts_l[k]:ends_l[k]]
        print(imgRow.shape)
        print(imgTextField.shape)
        cv2.imwrite(outputFileName,imgTextField)
        #img_rgb = cv2.cvtColor(imgTextField, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(imgTextField, config="--psm 7")
        #print(text)
        textClean=res = re.sub(r'[\x00-\x1f]', '', text)
        report+=inputFileName+"_"+str(i)+"_"+str(k)+".png,"+textClean+"\n"

    with open("report.txt", "w") as new_file:
        new_file.write(report)


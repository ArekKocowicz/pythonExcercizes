import cv2 as cv
import pytesseract
import argparse

window_title="ocr"
trackbar_resize_title="size"
trackbar_threshold_title="threshold"

def main(image):
    global src
    src = cv.imread(cv.samples.findFile(image))
    print(src.shape)
    if src is None:
        print('Could not open or find the image: ', image)
        exit(0)
    gray_image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    src=gray_image
    cv.namedWindow(window_title)
    cv.createTrackbar(trackbar_resize_title, window_title, 300, 1000, doOCR)
    cv.createTrackbar(trackbar_threshold_title, window_title, 200, 255, doOCR )
    cv.imshow(window_title, src)
    print(pytesseract.image_to_string(src, config="--psm 7"))
    cv.waitKey()

def doOCR(val):
    scale=cv.getTrackbarPos(trackbar_resize_title, window_title)
    #print(f"doOCR {scale}")
    fscale=scale/100
    thres=cv.getTrackbarPos(trackbar_threshold_title, window_title)
    resized=cv.resize(src, (0, 0), fx = fscale ,fy = fscale)
    _, binary = cv.threshold(resized, thres, 255, cv.THRESH_BINARY)
    cv.imshow(window_title, binary)
    print(pytesseract.image_to_string(binary, config="--psm 7"))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code for testing pytesseract')
    parser.add_argument('--input', help='Path to input image.', default='LinuxLogo.jpg')
    args = parser.parse_args()
    main(args.input)

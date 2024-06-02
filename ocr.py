import cv2 as cv
import pytesseract
import argparse

window_title="ocr"

def main(image):
    global src
    src = cv.imread(cv.samples.findFile(image))
    if src is None:
        print('Could not open or find the image: ', image)
        exit(0)
    cv.namedWindow(window_title)
    #cv.createTrackbar(title_trackbar_element_shape, title_erosion_window, 0, max_elem, erosion)
    #cv.createTrackbar(title_trackbar_kernel_size, title_erosion_window, 0, max_kernel_size, erosion)
    #cv.namedWindow(title_dilation_window)
    #cv.createTrackbar(title_trackbar_element_shape, title_dilation_window, 0, max_elem, dilatation)
    #cv.createTrackbar(title_trackbar_kernel_size, title_dilation_window, 0, max_kernel_size, dilatation)
    #erosion(0)
    #dilatation(0)
    cv.imshow(window_title, src)
    print(pytesseract.image_to_string(src, config="--psm 7"))
    print(pytesseract.image_to_boxes(src))
    cv.waitKey()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code for testing pytesseract')
    parser.add_argument('--input', help='Path to input image.', default='LinuxLogo.jpg')
    args = parser.parse_args()
    main(args.input)

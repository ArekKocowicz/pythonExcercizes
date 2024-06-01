import cv2
import pytesseract

fields=[]
fields.append({"name":"Measure", "x1":758, "x2":773, "y1":2, "y2":64})


inputFileName = "4700--00002.png"
inputImage = cv2.imread(inputFileName)

# Window name in which image is displayed 
 
print(pytesseract.image_to_boxes(inputImage))
print(pytesseract.image_to_string(inputImage))
 
# closing all open windows 
#cv2.destroyAllWindows()

cv2.imshow("test", inputImage) 
cv2.waitKey(0)
cv2.destroyAllWindows()

for field in fields:
    cropped_image=inputImage[field["x1"]:field["x2"], field["y1"]:field["y2"]]

    cv2.imshow("cropped_image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWoindows()



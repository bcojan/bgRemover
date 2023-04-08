import cv2
import json
import numpy

class Rectangle():
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def toJSON(self):
        return json.dumps(self.__dict__)
    
class ROIs():
    def __init__(self, main) -> None:
        self.main = main
        self.rois = []

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        
def roi_from_image(image):
    open_cv_image = numpy.array(image) 
    grayImage = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    cnts = cv2.findContours(grayImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    minY, minX = grayImage.shape[:2]
    rois = ROIs(Rectangle(minX, minY, 0, 0))
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        rois.main.x = min(x, rois.main.x)
        rois.main.y = min(y, rois.main.y)
        rois.main.width = max(w, rois.main.width)
        rois.main.height = max(h, rois.main.height)
        if w > 200 and h > 200:
            rois.rois.append(Rectangle(x,y,w,h)) 

    return rois
import cv2
import numpy as np
from datetime import datetime
from os import remove
from threading import Thread

ORIG_IMG_PATH = "./Images/orig.jpg"
PROC_IMG_PATH = "./Images/proc.jpg"
HIST_IMG_PATH = "./Images/history"
CROP_POINTS = ((72, 70), (680, 72), (675, 670), (62, 670))

class CameraController:

    GMF = 0

    def __init__(self, saveHistory = False) -> None:
        self.image = cv2.imread(ORIG_IMG_PATH)
        h, w = self.image.shape[:2]
        center = int((w - h)/2)
        self.image = self.image[0:h, center:w-center]
        if saveHistory:self.save(f"{HIST_IMG_PATH}/{datetime.now().strftime('%m-%d_%H-%M')}.jpg")

    
    def crop(self):
        height, width = self.image.shape[:2]
        src_pts = np.float32(CROP_POINTS)
        dst_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        self.image = cv2.warpPerspective(self.image, matrix, (width, height))
        return self

    def blur(self, attrs=(25, 25)):self.image = cv2.blur(self.image, attrs); return self

    def filter(self, filterAttr : list):
        hsv         = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask        = cv2.inRange(hsv, np.array(filterAttr[0]), np.array(filterAttr[1]))
        self.image  = cv2.bitwise_and(self.image, self.image, mask=mask)
        self.GMF    = cv2.countNonZero(mask)
        return self
    
    def calculate(self): return round((self.GMF/(self.image.shape[0]*self.image.shape[1])) * 100, 2)
    
    def save(self): cv2.imwrite(PROC_IMG_PATH, self.image)

    @staticmethod
    def new(image_path = None):
        Thread(target=CameraController._newImage, args=[image_path,]).start()
        # return CameraController._newImage(image_path)
            
        
    @staticmethod
    def delete():
        Thread(target=CameraController._deleteImage, args=[ORIG_IMG_PATH, ]).start()
        Thread(target=CameraController._deleteImage, args=[PROC_IMG_PATH, ]).start()

    @staticmethod
    def _newImage(imagePath = None):
        try:
            import picamera
            from time import sleep
            camera = picamera.PiCamera()
            sleep(2)
            if imagePath: camera.capture(imagePath)
            else: camera.capture(ORIG_IMG_PATH)
            camera.close()
            return True
        except: return False
    
    @staticmethod
    def _deleteImage(path):
        try: remove(path) 
        except: pass

if __name__ == "__main__":
    cm = CameraController()
    cm.crop()
    cm.filter([[22, 68, 72], [63, 255, 255]])
    currentGreen = cm.calculate()
    cm.save()





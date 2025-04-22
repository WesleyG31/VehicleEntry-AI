import easyocr
import torch
import cv2

class PlateOCR:
    def __init__(self):
        self.device = True if torch.cuda.is_available() else False
        self.reader=easyocr.Reader(['en'], gpu=self.device)

    
    def procces_image(self, image_to_process):

        grayscale_plate= cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
        grayscale_plate = cv2.resize(grayscale_plate, (300, 100))
        filtered = cv2.bilateralFilter(grayscale_plate, 11, 17, 17)
        thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 31, 5)
        return thresh

    def ocr_plate(self, cropped_plate):

        proccesed= self.procces_image(cropped_plate)
        results= self.reader.readtext(proccesed)
        
        if results:
            text= results[0][1]
            return text
        else:
            return None

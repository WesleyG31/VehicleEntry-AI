import torch
from ultralytics import YOLO
import cv2


class YoloDetector:
    def __init__(self, model_path, confidence_yolo=0.6):
        self.model=YOLO(model_path)
        self.confidence_yolo = confidence_yolo
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def detect_plate(self, frame):
        results= self.model.track(frame, persist=True, verbose=False, device=self.device, conf=self.confidence_yolo)

        for result in results:
            boxes= result.boxes
            if boxes is not None and len(boxes)>0:
                for box in boxes:
                    x1,y1,x2,y2= map(int,box.xyxy[0])
                    cropped_plate=frame[y1:y2,x1:x2]
                    track_id = int(box.id.item()) if box.id is not None else None
                    conf=float(box.conf[0])
                    return track_id,conf,cropped_plate, (x1, y1, x2, y2) 
        return None, None, None, None

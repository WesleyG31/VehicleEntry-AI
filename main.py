import os
import cv2

from detection.yolo_detector import YoloDetector
from utils.video_utils import save_video
from detection.ocr_detector import PlateOCR
from database.database import VehicleData
from sheets_conection.write_sheets import GoogleSheet_write
from temp_write.temp_write import RegistroTemporal


def main():

    print("Loading Models...")

    base_path = os.path.dirname(__file__)
    video_path = r"C:\All files\VehicleEntry-AI\data\test\vehicles.mp4"
    cap= cv2.VideoCapture(video_path)

    model_path= os.path.join(base_path,"models","yolov8n_plates.pt")
    data_path= os.path.join(base_path,"database","AUTOS_PERMITIDOS.xlsx")
    sheets_key_json= os.path.join(base_path,"key.json")

    frames_video=[]
    output_video_path_avi= os.path.join(base_path,"output","video_output.avi")
    output_video_path_mp4= os.path.join(base_path,"output","video_output.mp4")
    plates_detected = {}


    detector= YoloDetector(model_path, confidence_yolo=0.7) 
    reader= PlateOCR()
    data= VehicleData(file_path=data_path)
    conection_google_sheets= GoogleSheet_write(credentials_file=sheets_key_json,
                                                spreadsheet_name="vehiculos",
                                                worksheet_name="hoja 1")
    registro_temporal = RegistroTemporal(intervalo_segundos=30)

    print("starting video processing...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        #frame= cv2.flip(fram,1)

        track_id,conf,cropped_plate,bbox= detector.detect_plate(frame)
        #clase_yolo = "Placa" if class_id == 0 else "No Placa"

        if track_id not in plates_detected and cropped_plate is not None and cropped_plate.size > 0:
            plate_text= reader.ocr_plate(cropped_plate)
        
            if plate_text:
                info= data.get_info(plate_text)
                plates_detected[track_id] = info
                conection_google_sheets.write_events(info["placa"],info["propietario"],info["autorizado"],track_id)
                label_color= (0,255,0) if info["autorizado"] else (0,0,255)
                x1,y1,x2,y2=bbox
                cv2.rectangle(frame,(x1,y1),(x2,y2),label_color,1)
                cv2.putText(frame,f"{plate_text}, {conf:.2f}",(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,label_color,2)
            
        frames_video.append(frame.copy())

        cv2.imshow("Plate Detector",frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()  
    cv2.destroyAllWindows()
    save_video(frames_video,output_video_path_avi,output_video_path_mp4)
    print("Video saved successfully!")

if __name__ == "__main__":
    main()
    

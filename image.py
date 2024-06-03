import cv2
import time
from constants import Constants
from datetime import datetime
import requests

class SlotDetector:

    def __init__(self, image_path: str, slots: list, uid: str) -> None:
        self.parking_uid = uid
        self.image_path = image_path
        self.parking_slots = slots
        self.rect_width, self.rect_height = Constants.RECT_WIDTH, Constants.RECT_HEIGHT
        self.color = Constants.RECT_COLOR
        self.thick = Constants.RECT_THICKNESS
        self.threshold = Constants.THRESHOLD
        self.last_call_time = time.time()
        self.prevFreeslots = 0
        self.displayedImage = False

    def convert_grayscale(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = frame.copy()
        contour_image[:] = 0
        cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=2)
        return contour_image
    
    def mark_slots(self, frame, grayscale_frame, display_slots):
        freeslots=0
        for x, y in self.parking_slots:
            x1=x+10
            x2=x+self.rect_width-11
            y1=y+4
            y2=y+self.rect_height
            start_point, stop_point = (x1,y1), (x2, y2)

            crop=grayscale_frame[y1:y2, x1:x2]
            gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

            count=cv2.countNonZero(gray_crop)

            color, thick = [(0,255,0), 5] if count<self.threshold else [(0,0,255), 2]

            if count<self.threshold:
                freeslots = freeslots+1

            cv2.rectangle(frame, start_point, stop_point, color, thick)
        
        if display_slots:
            print(f"[INFO] - - {datetime.now().strftime('[%d/%b/%Y %H:%M:%S]')} 'No of free slots: {freeslots}' -")
            res = self.fetch_request({'uuid': self.parking_uid, 'slots_available': freeslots})
            if res:
                print("DB Updated")

    def fetch_request(self, params):
        try:
            
            response = requests.get('http://127.0.0.1:5000/api/v1/update_parking_info', params=params)

            if response.status_code == 200:
                res = response.json()
                if res["status"] == 'success':
                    return True
                return False
            else:
                print("Error: Status code", response.status_code)
                return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False
    
    def process_frame(self):
        frame = cv2.imread(self.image_path)
        if frame is None:
            print("Error reading image file")
            return

        grayscale_frame = self.convert_grayscale(frame)
        self.mark_slots(frame, grayscale_frame, display_slots=True)



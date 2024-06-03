import os
import cv2
import time
from image import SlotDetector
from constants import Constants


def capture_photos(camera_index=None, video_path=None, output_dir="photos"):
    start_time = time.time()
    photo_captured = False
    
    if camera_index is not None:
        cap = cv2.VideoCapture(camera_index)
    elif video_path is not None:
        cap = cv2.VideoCapture(video_path)
    else:
        print("Please provide either camera index or video path.")
        return

    if not cap.isOpened():
        print("Error opening video source.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"Video resolution: {frame_width}x{frame_height}")
    print(f"FPS: {fps}")
    
    os.makedirs(output_dir, exist_ok=True)

    photo_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame.")
            break
        
        time.sleep(1 / fps)
        
        time_diff = int(time.time() - start_time)

        if(time_diff % 5) == 0 and time_diff != 0:
            if not photo_captured:
                photo_count += 1
                photo_name = "photo.jpg"
                photo_path = os.path.join(output_dir, photo_name)
                cv2.imwrite(photo_path, frame)
                print(f"Photo captured: {photo_path}")
                detector = SlotDetector(photo_path, Constants.CAMERA_PARK_SLOTS, "0277f08e-ee78-11ee-a419-0534d864ffe7")
                detector.process_frame()
                photo_captured = True
        else:
            photo_captured = False

        cv2.imshow('Frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Parking Detector Setup")
    
    camera_index = 0
    video_path = "CarPark_AdobeExpress.mp4"
    
    capture_photos(video_path=video_path)

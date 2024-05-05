# Last Update: 2024/05/05
# Author: Luke Kaser
# Description: This program uses OpenCV to interact with the web camera. It includes functionality to capture video and process it in real-time.
# E-mail:qaz442200156@gmail.com

import os
import time
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from datetime import datetime

# opencv reference https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
# YT reference https://youtu.be/V62M9d8QkYM?feature=shared
print(f"OpenCv Version:{cv2.__version__}")

def get_current_time():
    return datetime.now().strftime('%Y_%m_%d-%H-%M-%S')

# ---------------------
# region OS dir process
# ---------------------

def get_file_dir(file_path):
    return os.path.dirname(file_path)

def create_dir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_filename_without_extension(path):
    base_name = os.path.basename(path)  # Get the filename with extension
    file_name_without_extension = os.path.splitext(base_name)[0]  # Remove the extension
    return file_name_without_extension
    
# ---------------------
# endregion
# ---------------------

# ---------------------
# region Core Cv Process
# ---------------------

def capture_frame(cap_machine):
    ret, frame = cap_machine.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None
    return frame

def process_mirror_frame(frame):
    if is_mirror_flip:
        '''            
        # cv2.flip(frame, 1) flip with y (horizontal flip)
        # cv2.flip(frame, 0) flip with x (vertical flip)
        # cv2.flip(frame, -1) flip with both x,y
        '''
        frame = cv2.flip(frame, 1)
    return frame
    
def display_frame(frame,detection_frame, title=None):
    if is_take_any_webcame_action or is_recording or is_time_recording:
        cv2.imshow("On Recording" if title is None else title, frame)
    else:
        cv2.imshow("On Detection" if title is None else title, detection_frame)

def get_new_video_writer(save_video):
    file_name = save_video.get_save_path()
    video = cv2.VideoWriter(file_name, video_fourcc,video_fps,(video_original_rect.width,video_original_rect.height))
    return file_name,video

def try_write_frame(frame):
    if is_recording and video is not None:
        video.write(frame)
    if is_time_recording and time_video is not None:
        time_video.write(frame)

def change_record_state(recording_flag, target_video, save_video, saved_filename):
    next_recording_flag = recording_flag is not True
    print("Start Recording" if next_recording_flag else "Stop Recording")
    
    if target_video is not None:
        target_video.release()
        
    if next_recording_flag:
        file_name,video = get_new_video_writer(save_video)
    else:
        print(f"video file saved at :{saved_filename}")
        video = None
        file_name = None
    return next_recording_flag, video, file_name

def release_resource(cap_machine):
    global video
    global time_video
    cap_machine.release()
    if video is not None:
        video.release()
    if time_video is not None:
        time_video.release()
    cv2.destroyAllWindows()
# ---------------------
# endregion
# ---------------------

# ---------------------
# region OpenCv Object Detection
# ---------------------
def object_detection(frame):
    if is_take_any_webcame_action or is_recording or is_time_recording:
        return frame,frame, None
    bbox, label, conf = cv.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)
    return frame,output_image,label

def process_object_detection(label):
    global time_video_recording_time_duration
    if label is None:
        return False
    
    '''    
    for item in label:
        Do something special when item is __
    '''
    return False

# ---------------------
# endregion
# ---------------------
    
# ---------------------
# region Actions(Record,Time Record, SnapShot)
# ---------------------

def process_recording():    
    global video
    global is_recording
    global video_filename
    is_recording,video,video_filename = change_record_state(is_recording,video,save_video_name, video_filename)

def process_time_recording():
    global time_video
    global is_time_recording
    global time_video_start_time
    global time_video_filename
    is_time_recording,time_video,time_video_filename = change_record_state(is_time_recording,time_video,save_time_video_name, time_video_filename)
    if is_time_recording:
        time_video_start_time = datetime.now()

def process_time_recording_passed_time():
    global time_video_recording_time_duration
    if not is_time_recording:
        return
    passed_time = datetime.now() - time_video_start_time
    if passed_time.total_seconds() > time_video_recording_time_duration:
        time_video_recording_time_duration = 0
        process_time_recording()
        cv2.destroyAllWindows()
    else:        
        print(f"Time remain:{(time_video_recording_time_duration - passed_time.total_seconds()):.2f}")

def take_snapshot():
    snapshot_filename = save_image_name.get_save_path()
    print(f"snapshot saved at :{snapshot_filename}")
    frame = capture_frame(cap_machine)
    if frame is None:
        return
    frame = process_mirror_frame(frame)
    cv2.imwrite(snapshot_filename,frame)

# ---------------------
# endregion
# ---------------------

# ---------------------
# region Keyboard Input
# ---------------------

def read_key():
    global time_video_recording_time_duration
    global is_take_any_webcame_action
    # Current keyboard input
    key = cv2.waitKey(1)
    if key != -1:# Show input key value
        print(f"Passed Key => int:{key} char:{chr(key)}")
    # if not passed any key will return -1 as default
    # ord('') turn key as int
    if key == ord('q'): # exit
        return True
    elif key == ord('r'): # start/stop recording
        is_take_any_webcame_action = True
        process_recording()
    elif key == ord('s'): # take snapshot
        is_take_any_webcame_action = True
        take_snapshot()
    elif not is_time_recording: # start/stop time recording
        if key == ord('0'):
            time_video_recording_time_duration = 10
        if key == ord('3'):
            time_video_recording_time_duration = 3
        if key == ord('5'):            
            time_video_recording_time_duration = 5
        if key == ord('8'):            
            time_video_recording_time_duration = 8
        if time_video_recording_time_duration > 0:
            is_take_any_webcame_action = True
            process_time_recording()
    if is_take_any_webcame_action:
        cv2.destroyAllWindows()
    return False

# ---------------------
# endregion
# ---------------------

# ---------------------
# region Class
# ---------------------
class Rect:
    def __init__(self,width,height):
        self.width = width
        self.height = height

class SaveFormat:
    def __init__(self,save_path,save_file_name,extension):
        self.SavePath = save_path
        self.SaveFileName = save_file_name
        self.Extension = extension
        # check dir        
        file_dir = get_file_dir(self.SavePath)
        create_dir_if_not_exists(file_dir)

    def get_save_path(self):
        return f'{os.path.join(self.SavePath,self.SaveFileName)}_{get_current_time()}.{self.Extension}'

# ---------------------
# endregion
# ---------------------

# ---------------------
# region Data
# ---------------------
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# --- Save File ---
save_video_name = SaveFormat('data/Video/','Video','avi')
save_time_video_name = SaveFormat('data/TimeVideo/','TimeVideo','avi')
save_image_name = SaveFormat('data/SnapShot/','SnapShot','jpg')
# --- Web Cam machine ---
cap_machine = cv2.VideoCapture(1)

# --- Frame Format ---
# Frame Size(Default)
video_original_rect = Rect(int(cap_machine.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap_machine.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# Framerate
video_fps = 30.0
# Video format
video_fourcc = cv2.VideoWriter_fourcc(*'XVID')

# --- Recording ---
# Video writer
video = None
# Current Video file name
video_filename = None

# --- Time Recording ---
# Time Video writer
time_video = None
# Current Time Video file name
time_video_filename = None
# The time video start recording time
time_video_start_time = None
# The time video length (second)
time_video_recording_time_duration = 0

# --- Base Settings ---
# Is On recording or not
is_recording = False
# Is On time recording or not
is_time_recording = False
# Is use mirror frame or not
is_mirror_flip = True
# Is on take snapshot
is_take_any_webcame_action = False

# ---------------------
# endregion
# ---------------------

def main():
    global is_take_any_webcame_action
    if not cap_machine.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        frame = capture_frame(cap_machine)
        if frame is None:
            break
                    
        if is_take_any_webcame_action:
            is_take_any_webcame_action = False
            continue
        # Check is use mirror to flip frame
        frame = process_mirror_frame(frame)

        # Object Detection
        frame,detection_frame,label = object_detection(frame)

        # Process object detection and do something
        if process_object_detection(label):
            cv2.destroyAllWindows()
            continue

        # If on recording and try write current frame into video file
        try_write_frame(frame)
        
        # If on time recording do time pass
        process_time_recording_passed_time()

        # Show live video 
        display_frame(frame, detection_frame)

        # Check keyboard input
        if read_key():
            break

    # Release eversything if job is finished
    release_resource(cap_machine)

if __name__ == "__main__":
    main()
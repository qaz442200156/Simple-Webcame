# WebCamera Program

This program uses OpenCV to interact with the web camera. It includes functionality to capture video, object detection, process it in real-time, and handle time-based recording.

## Dependencies
- Python 3
- OpenCV (cv2)
- cvlib

### Prerequisites

You will need Python 3 and the following libraries installed:

- OpenCV
- cvlib

You can install these using pip:

```bash
pip install opencv-python cvlib
```

## Features
- Real-time video capture: The program captures video from the web camera in real-time.
- Time-based recording: The program includes functionality to handle time-based recording. It checks if a certain amount of time has passed and performs some action if it has.
- Keyboard input: The program checks for keyboard input to control its operation. If a certain key is pressed, the program ends.
- Resource management: The program releases all used resources when the job is finished.

## Usage
1. Install the dependencies: You need Python 3 and OpenCV installed on your machine to run this program.
2. Run the `WebCamera.py` script to start the program.
3. The program will start capturing video from your web camera.
4. Press the specified key to end the program.

- Key Map
    - 3 : Take 3 seconds short video
    - 5 : Take 5 seconds short video
    - 8 : Take 8 seconds short video
    - 0 : Take 10 seconds short video
    - s : Take Snapshot
    - r : Start/Stop Recoding
    - q : Exit

## Custom Object Detection Process

```Python
def process_object_detection(label):
    global time_video_recording_time_duration
    if label is None:
        return False
    
    '''    
    for item in label:
        Do something special when item is __
    '''
    return False
```


## References
- [OpenCV Documentation](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
import cv2 
  
def FrameCapture(path): 
    
    vidObj = cv2.VideoCapture(path) 
    
    count = 0
    
    success = 1
  
    while success: 

        success, image = vidObj.read() 
  
        cv2.imwrite("frame%d.jpg" % count, image)
  
        count += 1
  
if __name__ == '__main__': 

    FrameCapture("bad_apple.mp4")

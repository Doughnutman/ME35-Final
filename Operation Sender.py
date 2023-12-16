import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

broker_address='10.243.87.114'
client = mqtt.Client("DL_CPU") 
client.connect(broker_address) 
url = 'http://10.243.95.124:4747/video'
cap = cv2.VideoCapture(url)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

def find_object_center(frame, lower_bound, upper_bound):
    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Threshold the image to get only the object of interest
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    # Find contours in the binary image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the contour with the maximum area
        max_contour = max(contours, key=cv2.contourArea)
        # Calculate the centroid (center) of the object
        M = cv2.moments(max_contour)
        center_x = int(M['m10'] / (M['m00'] + 1e-5))  # Adding a small value to avoid division by zero
        center_y = int(M['m01'] / (M['m00'] + 1e-5))
        return center_x, center_y
    else:
        return None, None

def find_blue(frame):
# Find the center of the blue object and assign origin
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    blue_origin_x, blue_origin_y = None, None
    blue_center_x, blue_center_y = find_object_center(frame, lower_blue, upper_blue)
    if blue_center_x is not None:
        blue_origin_x, blue_origin_y = blue_center_x, blue_center_y
    return blue_center_x, blue_center_y
        
def find_green(frame):
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])
    green_center_x, green_center_y = find_object_center(frame, lower_green, upper_green)
    return green_center_x, green_center_y
    
def create_frame(name):
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        exit()
    #find green and blue
    bluex, bluey = find_blue(frame)
    greenx, greeny = find_green(frame)
     
    #create black frame
    frame_with_dots = np.zeros_like(frame)
    #create detection dots
    if bluex is not None:
        cv2.circle(frame_with_dots, (bluex, bluey), 5, (255, 0, 0), -1)  # Blue dot
    if greenx is not None:
        cv2.circle(frame_with_dots, (greenx, greeny), 5, (0, 255, 0), -1)
    #show dotted image
    cv2.imshow('Dotted frame',frame_with_dots)
    cv2.waitKey(10)
        
    return frame_with_dots, bluex, bluey, greenx, greeny

def set_movement(bx, by, gx, gy, xscale, yscale):
    xmove = (bx-gx)/xscale
    ymove = (by-gy)/yscale
    print("x-move: " + str(xmove) + "\ny-move: " + str(ymove))
    #publish the coordinates via mqtt
    client.publish("coord", str(xmove)+","+str(ymove))
   
def main():
    # Check if the camera opened successfully
    # Measure and print the camera frame dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    print(f"Camera Frame Dimensions: {frame_width} x {frame_height}")
    #get the initial frame and center coordinates
    before, bx1, by1, gx1, gy1 = create_frame('Before')
    #publish and pick up at the coordinates
    set_movement(bx1,by1,gx1,gy1,2,2)
    count = 0
    #wait for the piece to be picked up
    while True:
        ret4, frame4 = cap.read()
        cv2.imshow('Video',frame4)
        # checking every ms for 'count' value
        if cv2.waitKey(1) & int(count > 5) :
            break
        count += 0.01 # increment counter 
        print(count)
    print("I am actually screaming!")
    # find new positions of center coordinates
    after, bx2, by2, gx2, gy2 = create_frame('After')
    #check if there the blue has moved
    if abs(bx1-bx2) > 20 and abs(by1-by2) > 20:
        print('Operation Successful')
    else:
        print("Patient is dead")
        
    #release resources
    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()

main()

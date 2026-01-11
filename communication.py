# ESP32-CAM pill detection and pixel comparison code
# uses camera stream from ESP32-CAM and arduino IDE to capture stills


# IMPORTS
# ------------------------------
import requests 
# send http requests to cam, library for interacting w/ things over the internet
# allows us to use python to ask the cam for an image easily
import numpy as np 
# math library to handle arrays of image numbers (how bright it is)
import cv2 
# use to decode camera images, comp. pixel changes
import time 
import os # files
# ------------------------------


# CONSTANTS
ESP32CAM_IP = "172.20.10.9" # esp32 cameras ip
images = [] # list holding image brightness arrays
detection_enabled = True # tracks pill detection



# CAPTURE IMAGES
# ------------------------------
def capture_image(filename):
  # captures 1 grayscale image at a time from the esp32 camera and 
  # saves it to the file.

  capture_url = f"http://{ESP32CAM_IP}/capture" # captures pic and returns jpg image
  
  # requests image from capture we took above
  rsp = requests.get(capture_url) 

  raw = rsp.content
  img_bytes = np.frombuffer(raw, np.uint8)
  decoded_img = cv2.imdecode(img_bytes, cv2.IMREAD_GRAYSCALE)
  img = decoded_img

  # safety (decoding error check)
  if img is None:
    print("safety check failed: decoding image error.")
    return None
  
  # save image 2 disk
  cv2.imwrite(filename, img)
  print(f"-- image saved as {filename} -- \n")

  return img
# ------------------------------





# COMPARE IMAGES
# ------------------------------
def compare_images(img1, img2, threshold=5000):
  # checks if enough pixels changed between each image.

  # make sure theres images
  if img1 is None or img2 is None:
    return False
  
  # pixel x pixel diff
  difference = cv2.absdiff(img1, img2) # num of diff pixels
  numPix_change = np.sum(difference > 20) # check for enough change

  print(f"pixel comp. tracker: {numPix_change} pixels changed \n")
  return numPix_change > threshold # returns True if enough pixels changed
# ------------------------------




# IMAGE BUFFER
# ------------------------------
def initialize_images():
  # first set of images for comparison.

  global images
  images = []

  # initial images for rolling buffer
  for i in range(3):
    filename= f"cam_frame_{i+1}.jpg"
    img = capture_image(filename)
    images.append(img)
# ------------------------------



# MAIN DETECTION
# ------------------------------
def check_for_pill():
  # tracks whether a pill has been 'taken'.
  # returns True if pill has been detected for the first time, and returns False otherwise.
  
  global images, detection_enabled

  # skip detection if system is disabled
  if detection_enabled == False:
    # print ("detection dis.")
    return False

  # make sure we have at least 2 images to compare
  if len(images) < 2:
    return False

  # compare two most recent images
  if compare_images(images[-2], images[-1]):
    print(f"!! motion detected !! \n")
    return True
  
  # remove 3rd image file (oldest)
  if os.path.exists("cam_frame_1.jpg"):
    os.remove("cam_frame_1.jpg")

  # shift img buffer
  images = images[1:]

  # switch around image names to fix order
  for i in range(len(images)):
    old = f"cam_frame_{i+2}.jpg"
    new = f"cam_frame_{i+1}.jpg"

    if os.path.exists(new):
      os.remove(new)
    os.rename(old, new)

  # capture new image and add it to the list
  new_file = f"cam_frame_{len(images)+1}.jpg"
  images.append(capture_image(new_file))

  return False

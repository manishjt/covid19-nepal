import numpy as np
import cv2
import os

N = 100
image_location = "../results/results_road/without_lines/"
image_name = "covid000"
images = []
for i in range(N):
    images.append(cv2.imread(image_location+image_name+str(i)+".png"))

height,width,layers=images[1].shape

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video=cv2.VideoWriter(image_location+'video.avi',fourcc,1,(width,height))

for i in range(N):
    video.write(images[i])

cv2.destroyAllWindows()
video.release()

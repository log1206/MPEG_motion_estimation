import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
from datetime import datetime

img_r = cv2.imread('caltrain007.tiff',0) ##different place need to relink
img_t = cv2.imread('caltrain008.tiff',0)


block_size =8
d = 30 ##range for search
width = 512 ## original width
height = 400 ## original height
width_d = width//block_size ## divided width
height_d = height//block_size ## divided height


small = 10000 ###current smallest SSD
temp_s = 0
temp_r = np.zeros((block_size,block_size),float)
temp_t = np.zeros((block_size,block_size),float)
temp = np.zeros((block_size,block_size),float)
current_small = np.zeros((block_size,block_size),float)

 
img_log = np.zeros((img_r.shape[0],img_r.shape[1]), float)
img_exh = np.zeros((img_r.shape[0],img_r.shape[1]), float)

img_exh = img_t-img_r
img_log = img_t-img_r


def calSSD():
    global temp
    global temp_s
    global small
    global current_small
    temp = temp_t - temp_r
    temp_s = np.sum(temp**2)

    if(temp_s <small):
        small =temp_s
        
        current_small[:,:] = temp[:,:] +128
        print(current_small)

### foe exhaustive time
time_exh =datetime.now()
for i in range(height_d):
    for j in range(width_d):
        temp_t[:,:] = img_t[i*block_size:i*block_size+8,j*block_size:j*block_size+8]
        small =10000
        for a in range(d+1):
            for b in range(d+1):

                ###up left
                if(i*block_size-a >= 0 and j*block_size-b >= 0):
                    temp_r[:,:] = img_r[i*block_size-a:i*block_size+8-a,j*block_size-b:j*block_size+8-b]
                    calSSD()
                ###up right
                if(i*block_size-a >= 0 and j*block_size+b+block_size <=width):
                    temp_r[:,:] = img_r[i*block_size-a:i*block_size+8-a,j*block_size+b:j*block_size+8+b]
                    calSSD()
                ###down left
                if(i*block_size+a+block_size <= height and j*block_size-b >= 0):
                    temp_r[:,:] = img_r[i*block_size+a:i*block_size+8+a,j*block_size-b:j*block_size+8-b]
                    calSSD()
                ###down right
                if(i*block_size+a+block_size <= height and j*block_size+b+block_size <=width):
                    temp_r[:,:] = img_r[i*block_size+a:i*block_size+8+a,j*block_size+b:j*block_size+8+b]
                    calSSD()
        img_exh[i*block_size:i*block_size+8,j*block_size:j*block_size+8] = current_small[:,:]

time_exh = datetime.now() - time_exh
print(img_exh)
print(time_exh)
cv2.imshow('exh', img_exh)
cv2.waitKey(0)
cv2.destroyAllWindows()

### for logarithm
time_log = datetime.now()

temp_up_m =np.zeros((block_size,block_size),float)
temp_down_m =np.zeros((block_size,block_size),float)
temp_left_m = np.zeros((block_size,block_size),float)
temp_right_m =np.zeros((block_size,block_size),float)
for i in range(height_d):
    for j in range(width_d):
        t_d = d//2
        small = 10000
        dir =0
        center_x = j * block_size
        center_y = i * block_size
        temp_t[:,:] = img_t[i*block_size:i*block_size+8,j*block_size:j*block_size+8]
        while t_d > 1:
            if center_y - t_d >= 0:    
                temp_up_m[:,:] = img_r[center_y-t_d:center_y-t_d+8,center_x:center_x+8] ###up
                temp = temp_t - temp_up_m
                temp_s = np.sum(temp**2)

                if(temp_s <small):
                    small =temp_s
                    center_y = center_y -t_d
                    current_small[:,:] = temp[:,:] +128
    
            if center_y + t_d + 8 <= height:    
                temp_down_m[:,:] = img_r[center_y+t_d:center_y+t_d+8,center_x:center_x+8] ###down
                temp = temp_t - temp_down_m
                temp_s = np.sum(temp**2)

                if(temp_s <small):
                    small =temp_s
                    center_y = center_y +t_d
                    current_small[:,:] = temp[:,:] +128

            if center_x - t_d >= 0:    
                temp_left_m[:,:] = img_r[center_y:center_y+8,center_x-t_d:center_x-t_d+8] ###left
                temp = temp_t - temp_left_m
                temp_s = np.sum(temp**2)

                if(temp_s <small):
                    small =temp_s
                    center_x = center_x -t_d
                    current_small[:,:] = temp[:,:] +128
            if center_x + t_d + 8 <= width:    
                temp_right_m[:,:] = img_r[center_y:center_y+8,center_x+t_d:center_x+t_d+8] ###right
                temp = temp_t - temp_right_m
                temp_s = np.sum(temp**2)

                if(temp_s <small):
                    small =temp_s
                    center_x = center_x +t_d
                    current_small[:,:] = temp[:,:] +128
            t_d = t_d//2
        ### compare nine around
        if center_y -1 >=0:
            temp_r[:,:] = img_r[center_y-1:center_y-1+8,center_x:center_x+8] ###up
            calSSD()
            if center_x -1 >=0:
                temp_r[:,:] = img_r[center_y-1:center_y-1+8,center_x-1:center_x-1+8] ###up
                calSSD()
            if center_x +1 +8 <=width_d:
                temp_r[:,:] = img_r[center_y-1:center_y-1+8,center_x+1:center_x+1+8] ###up
                calSSD()
        if center_x -1 >=0:
            temp_r[:,:] = img_r[center_y:center_y+8,center_x-1:center_x-1+8] ###up
            calSSD()
        if center_x +1 +8 <=width_d:
            temp_r[:,:] = img_r[center_y:center_y+8,center_x+1:center_x+1+8] ###up
            calSSD()
        
        if center_y +1 +8 <= height:
            temp_r[:,:] = img_r[center_y+1:center_y+1+8,center_x:center_x+8] ###up
            calSSD()
            if center_x -1 >=0:
                temp_r[:,:] = img_r[center_y+1:center_y+1+8,center_x-1:center_x-1+8] ###up
                calSSD()
            if center_x +1 +8 <=width_d:
                temp_r[:,:] = img_r[center_y+1:center_y+1+8,center_x+1:center_x+1+8] ###up
                calSSD()
        img_log[i*block_size:i*block_size+8,j*block_size:j*block_size+8] = current_small[:,:]
        
    
time_log = datetime.now() - time_log
print(img_log)
print(time_log)
cv2.imshow('log', img_log)
cv2.waitKey(0)
cv2.destroyAllWindows()   
        
       

     
        
       


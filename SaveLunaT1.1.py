import cv2
import numpy as np


# To identify the borders of a table using various different methods from scratch.
# Various methods :
'''

1. Sobel Detector
2. Laplacian based detector
3. Canny edge detector 

'''
#Reading and Resizing the image
img = cv2.imread("table.png")
img = cv2.resize(img , None , fx=0.5 , fy = 0.5)
cv2.imshow("Original Table",img)

#Blurring the image using Gaussian blur to clean up the noise using (5*5) size kernel
gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
gray_img = cv2.GaussianBlur( img , (5,5) , 0.5)

#Canny edge detection

canny_img = cv2.Canny(img , 50 , 200 , 2)


#Sobel Edge Detection
sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)

sobel_combined = cv2.addWeighted(cv2.convertScaleAbs(sobel_x), 0.5, cv2.convertScaleAbs(sobel_y), 0.5, 0)

#Laplacian Edge Detection

laplacian = cv2.Laplacian(gray_img,cv2.CV_64F)

'''#Now implementing hough line transform on these images 
sobel_combined_uint8 = cv2.convertScaleAbs(sobel_combined)

# Apply Hough Line Transform
lines = cv2.HoughLines(sobel_combined_uint8, 1, np.pi / 180, 150)  # Adjust the last parameter as needed

# Draw the detected lines on a copy of the original image
img_with_lines = img.copy()
if lines is not None:
    for rho, theta in lines[:, 0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img_with_lines, (x1, y1), (x2, y2), (0, 0, 255), 2)
'''

#Probablistic hough transform

linesP = cv2.HoughLinesP(canny_img, 1, np.pi / 180, 50, None, 50, 10)

# Draw the lines
'''if linesP is not None:
    for i in range(0, len(linesP)): 
        l = linesP[i][0]
        cv2.line(img, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)'''



# Extend the lines
if linesP is not None:
    for line in linesP:
        x1, y1, x2, y2 = line[0]
        # Calculate the direction vector of the line
        dx = x2 - x1
        dy = y2 - y1
        # Extend the line in both directions
        extended_line1 = (int(x1 - 1000 * dx), int(y1 - 1000 * dy))
        extended_line2 = (int(x2 + 1000 * dx), int(y2 + 1000 * dy))
        # Draw the extended line
        cv2.line(img, extended_line1, extended_line2, (0, 0, 255), 3, cv2.LINE_AA)




#Displaying the original Image
cv2.imshow('Edge_Table',canny_img)
cv2.imshow('Original Image',img)
cv2.waitKey(0)
cv2.destroyAllWindows
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load left and right images
left_img = cv2.imread("left.png", cv2.IMREAD_GRAYSCALE)
left_img = cv2.resize(left_img, None, fx=0.5, fy=0.5)

right_img = cv2.imread("right.png", cv2.IMREAD_GRAYSCALE)
right_img = cv2.resize(right_img, None, fx=0.5, fy=0.5)

# Calculate disparities using SIFT
sift = cv2.SIFT_create()

keypoints_left, descriptors_left = sift.detectAndCompute(left_img, None)
keypoints_right, descriptors_right = sift.detectAndCompute(right_img, None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(descriptors_left, descriptors_right, k=2)

good_matches = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good_matches.append(m)

disparities = []
for match in good_matches:
    left_pt = keypoints_left[match.queryIdx].pt
    right_pt = keypoints_right[match.trainIdx].pt
    disparity = right_pt[0] - left_pt[0]
    disparities.append(disparity)

# Normalize disparities
min_disparity = min(disparities)
max_disparity = max(disparities)
normalized_disparities = [(d - min_disparity) / (max_disparity - min_disparity) for d in disparities]

# Create colormap
colormap = plt.cm.jet

# Apply colormap to normalized disparities
heatmap = colormap(normalized_disparities)

# Reshape heatmap to match the left image size
heatmap = cv2.resize(heatmap, (left_img.shape[1], left_img.shape[0]))


# Convert heatmap to BGR format for compatibility with OpenCV
heatmap = (heatmap * 255).astype(np.uint8)

# Overlay heatmap on left image
alpha = 0.5  # Set transparency level (adjust as needed)
overlay = cv2.addWeighted(left_img[..., np.newaxis], 1-alpha, heatmap, alpha, 0)

colormap_jet = plt.cm.jet
colored_image = colormap_jet(overlay)

# Convert the RGBA image to BGR format for OpenCV compatibility
colored_image_bgr = cv2.cvtColor((colored_image[:, :, :3] * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)


cv2.imshow("Colored Image", colored_image_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()








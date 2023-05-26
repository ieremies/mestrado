import cv2
import numpy as np
import sys


def save(file, img):
    # turn back to gray scale
    aux = img.copy()
    aux[aux == 0] = 255
    aux[aux == 1] = 0
    cv2.imwrite(file, aux)


img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
img[img == 0] = 1  # all black pixels to 1
img[img == 255] = 0  # all whites pixels to 0

# print img shape
print(img.shape)


kernel1 = np.ones((1, 10), np.uint8)
img1 = cv2.dilate(img, kernel1, iterations=1)
# save("line1.png", img1)
# img1 = cv2.erode(img1, kernel1, iterations=1)
# save("line2.png", img1)

kernel2 = np.ones((10, 1), np.uint8)
img2 = cv2.dilate(img1, kernel2, iterations=1)
# save("line3.png", img2)
# img2 = cv2.erode(img2, kernel2, iterations=1)
# save("line4.png", img2)

# bitwise and
# img = cv2.bitwise_and(img1, img2)
# save("line5.png", img)

# closing operation
kernel = np.ones((1, 3), np.uint8)
img = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, kernel)

nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    img, None, None, None, 8, cv2.CV_32S
)

img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
for i in range(nlabels):
    x, y, w, h = stats[i][:4]
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imwrite(sys.argv[1].split(".")[0] + "out.png", img)

# save("line_out.png", img)

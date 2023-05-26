import cv2
import numpy as np


def save(file, img):
    """
    Function used to save the image midway throught our process.
    """
    # turn back to gray scale
    aux = img.copy()
    aux[aux == 0] = 255
    aux[aux == 1] = 0
    cv2.imwrite(file, aux)


def percentage(img) -> float:
    """
    Return the percentage of black pixels inside the image.
    """
    black = np.count_nonzero(img == 0)
    total = img.shape[0] * img.shape[1]
    return round(black / total, 2)


def h_transitions(img) -> int:
    """
    Returns the number of horizontal transitions of color.
    TODO tá errado, conferir com oq ue ele pediu
    """
    transitions = 0
    for j in range(crop.shape[0] - 1):
        if crop[j][crop.shape[1] // 2] != crop[j + 1][crop.shape[1] // 2]:
            transitions += 1
    return transitions


def v_transitions(img) -> int:
    """
    Returns the number of horizontal transitions of color.
    TODO tá errado, conferir com oq ue ele pediu
    """
    transitions = 0
    for j in range(crop.shape[1] - 1):
        if crop[crop.shape[0] // 2][j] != crop[crop.shape[0] // 2][j + 1]:
            transitions += 1
    return transitions


# Read the image
img = cv2.imread("bitmap.pbm", cv2.IMREAD_UNCHANGED)
img[img == 0] = 1  # all black pixels to 1
img[img == 255] = 0  # all whites pixels to 0

# Apply steps 1 and 2
kernel1 = np.ones((1, 100), np.uint8)
img1 = cv2.dilate(img, kernel1, iterations=1)
img1 = cv2.erode(img1, kernel1, iterations=1)
save("step2.png", img1)

# Apply steps 3 and 4
kernel2 = np.ones((200, 1), np.uint8)
img2 = cv2.dilate(img, kernel2, iterations=1)
img2 = cv2.erode(img2, kernel2, iterations=1)
save("step4.png", img2)

# bitwise and (step 5)
img = cv2.bitwise_and(img1, img2)
save("step5.png", img)

# closing operation
kernel = np.ones((1, 30), np.uint8)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
save("step6.png", img)

# detect connected components
nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    img, None, None, None, 8, cv2.CV_32S
)

# read original image
img = cv2.imread("bitmap.pbm", cv2.IMREAD_UNCHANGED)

# Gether information to filter out non-text lines
text = []
for i in range(nlabels):
    # (x,y) of topleft corner
    # (width, height) of the rect
    # b = number of black pixels
    x, y, w, h, b = stats[i][:5]
    # crop the image
    crop = img[y : y + h, x : x + w]

    text.append([x, y, w, h, b])

    # compute the percentage of black pixels
    text[-1].append(percentage(crop))

    # compute the number of vertical transitions
    text[-1].append(v_transitions(crop))

    # compute the number of horizontal transitions
    text[-1].append(h_transitions(crop))

# Text has to have height between 20 and 50 and percentage of black pixels
# between 10% and 40%.
text = [comp for comp in text if 20 < comp[3] < 50 and 0.1 < comp[5] < 0.4]


def detect_words(img):
    """
    Returns the connected components with stats of the words
    in the line in img.
    """
    img[img == 0] = 1  # all black pixels to 1
    img[img == 255] = 0  # all whites pixels to 0

    kernel1 = np.ones((1, 10), np.uint8)
    img = cv2.dilate(img, kernel1, iterations=1)

    kernel2 = np.ones((10, 1), np.uint8)
    img = cv2.dilate(img, kernel2, iterations=1)

    kernel3 = np.ones((1, 3), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel3)

    return cv2.connectedComponentsWithStats(img, None, None, None, 8, cv2.CV_32S)


words = []
for line in text:
    x, y, w, h = line[:4]
    crop = img[y : y + h, x : x + w]
    _, _, stats, _ = detect_words(crop.copy())
    for word in stats:
        # The connected componnents algorithm always returns a component
        # with the hole image. We discard it unless it only has one word in it.
        if (
            word[0] == 0
            and word[1] == 0
            and word[2] == w
            and word[3] == h
            and len(stats) > 2
        ):
            continue
        # We need to add the x,y coordinates of the line to those for the word.
        words.append([x + word[0], y + word[1], word[2], word[3], word[4]])


# Draw the bounding boxes
img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
for word in words:
    x, y, w, h = word[:4]
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
for line in text:
    x, y, w, h = line[:4]
    # we give a space of 2 pixels for the bounding box of lines
    # in order to not overlap with the words boxes.
    img = cv2.rectangle(img, (x - 2, y - 2), (x + w + 2, y + h + 2), (0, 255, 0), 2)

print(f"Number of lines = {len(text)}.")
print(f"Number of words = {len(words)}.")

cv2.imwrite("out.png", img)

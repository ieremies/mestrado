import cv2  # pip install opencv-contrib-python
import numpy as np


def lin_global(img, T=128):
    _, img_thresholded = cv2.threshold(img, T, 255, cv2.THRESH_BINARY)
    return img_thresholded


def otsu(img):
    _, img_thresholded = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_thresholded


def bernsen(img, window_size=25, contrast_threshold=5):
    return cv2.ximgproc.threshold_local(
        img,
        window_size,
        cv2.THRESH_BINARY,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        contrast_threshold,
    )


def niblack(img):
    return cv2.ximgproc.niBlackThreshold(img, 255, cv2.THRESH_BINARY, 7, 0.1)


def sauvola(img):
    return cv2.ximgproc.niBlackThreshold(
        img, 255, cv2.THRESH_BINARY, 7, 0.1, cv2.ximgproc.BINARIZATION_SAUVOLA
    )


def contraste(img, window_size=25, use_max=True):
    if use_max:
        _, img_thresholded = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    else:
        _, img_thresholded = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
    return img_thresholded


def media(img, window_size=25, contrast_threshold=5):
    return cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        window_size,
        contrast_threshold,
    )


def mediana(img, window_size=25, contrast_threshold=5):
    return cv2.adaptiveThreshold(
        img,
        255,
        cv2.ADAPTIVE_THRESH_MEDIAN_C,
        cv2.THRESH_BINARY,
        window_size,
        contrast_threshold,
    )

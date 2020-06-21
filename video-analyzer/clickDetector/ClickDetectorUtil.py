import os
import cv2
import numpy as np
from skimage.measure import compare_ssim
import imutils


def extract_action_img(frame, x1, y1, x2, y2):
    """Use coordinates of detected click and extract the region around the image."""
    height, width, _ = frame.shape

    y1_new = y1 - 40
    if y1_new < 0:
        y1_new = 0

    x1_new = x1 - 40
    if x1_new < 0:
        x1_new = 0

    y2_new = y2 + 40
    if y2_new > height:
        y2_new = height

    x2_new = x2 + 40
    if x2_new > width:
        x2_new = width

    return y1_new, y2_new, x1_new, x2_new

def apply_region_filter(before, after):
    before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(before_gray, after_gray, full=True)
    diff = (diff * 255).astype("uint8")

    bin = cv2.Canny(diff, 0, 100, apertureSize=5)
    cnts = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    before_region = np.zeros(before.shape, np.uint8)
    after_region = np.zeros(after.shape, np.uint8)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 50:
            x, y, w, h = cv2.boundingRect(c)
            before_region[y:y + h, x:x + w] = before[y:y + h, x:x + w]
            after_region[y:y + h, x:x + w] = after[y:y + h, x:x + w]

    return before_region, after_region


def count_files_in_dir(before_dir):
    return len([name for name in os.listdir(before_dir) if os.path.isfile(os.path.join(before_dir, name))])

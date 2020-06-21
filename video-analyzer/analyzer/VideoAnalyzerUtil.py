import numpy as np
import imutils
import cv2
import sys
from clickDetector.ClickDetectorUtil import apply_region_filter


class VideoAnalyzerProcessError(Exception):
    """ Raised when VideoAnalyzer is not able to process the current video. """
    pass


def update_gui_or_log(msg, status, process_clb=None):
    if process_clb is not None:
        process_clb.emit(status, msg)
    else:
        print(f"{status}% processed, MESSAGE {msg}")


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

    return frame[y1_new:y2_new, x1_new:x2_new, :]


def transform(img, threshold1, threshold2=200):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(np.uint8(img), threshold1, threshold2)


def find_cursor(frame, cursor_template):
    found = None

    frame = transform(frame, 50)
    cursor_template = transform(cursor_template, 150)

    (tH, tW) = cursor_template.shape[:2]
    for scale in np.linspace(0.5, 0.9, 50)[::-1]:
        resized_cursor = imutils.resize(cursor_template, width=int(cursor_template.shape[1] * scale))
        result = cv2.matchTemplate(frame, resized_cursor, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

        if found is None or maxVal > found[0]:
            (tW, tH) = resized_cursor.shape[:2]
            found = (maxVal, maxLoc)

    (_, maxLoc) = found
    (startX, startY) = (int(maxLoc[0]), int(maxLoc[1]))
    (endX, endY) = (int((maxLoc[0] + tH)), int((maxLoc[1] + tW)))

    return startX, startY, endX, endY


def reshape(before_frame, after_frame):
    before_region = np.expand_dims(before_frame, axis=0)
    before_region = before_region.astype('float32')
    before_region /= 255.0

    after_region = np.expand_dims(after_frame, axis=0)
    after_region = after_region.astype('float32')
    after_region /= 255.0
    return before_region, after_region


def preprocess_frames(before, after, width, height):
    before = cv2.cvtColor(before, cv2.COLOR_BGR2RGB)
    after = cv2.cvtColor(after, cv2.COLOR_BGR2RGB)

    before = cv2.resize(before, (width, height))
    after = cv2.resize(after, (width, height))

    before_region, after_region = apply_region_filter(before, after)
    return reshape(before_region, after_region)


# --------- EXTRACT button exact ----------------
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                binary = cv2.Canny(gray, 0, 100, apertureSize=5)
                binary = cv2.dilate(binary, None)
            else:
                _retval, binary = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)

            contours, _hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)

    return squares


def find_nearest(squares, mouse_pos=(0, 0)):
    min_dist_x = 1000
    min_dist_y = 1000
    result = None
    for square in squares:
        dist_x = mouse_pos[0] - square[0][0]
        dist_y = mouse_pos[1] - square[0][1]

        if 0 < dist_x and 0 < dist_y and (dist_x <= min_dist_x or dist_y <= min_dist_y):
            if dist_y + dist_x < min_dist_y + min_dist_x:
                min_dist_x = mouse_pos[0] - square[0][0]
                min_dist_y = mouse_pos[1] - square[0][1]
                result = square

    # x1, y1, x2, y2
    return result[0][0], result[0][1], result[2][0], result[2][1]


def extract_button(img, mouse_pos):
    squares = find_squares(img)
    x1, y1, x2, y2 = find_nearest(squares, mouse_pos)
    return img[y1:y2, x1:x2]

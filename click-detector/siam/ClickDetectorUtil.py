import os
import cv2
import imutils
import numpy as np
from skimage.measure import compare_ssim
from tensorflow.keras import layers
from tensorflow.keras.models import Model


def count_files_in_dir(before_dir):
    return len([name for name in os.listdir(before_dir) if os.path.isfile(os.path.join(before_dir, name))])


def create_conv_layer(input_img, input_shape):
    model = layers.Conv2D(32, (3, 3), input_shape=input_shape)(input_img)
    model = layers.BatchNormalization()(model)
    model = layers.Activation("relu")(model)
    model = layers.MaxPooling2D((2, 2))(model)

    model = layers.Conv2D(32, (3, 3))(model)
    model = layers.BatchNormalization()(model)
    model = layers.Activation("relu")(model)
    model = layers.MaxPooling2D((2, 2))(model)

    model = layers.Conv2D(64, (3, 3))(model)
    model = layers.BatchNormalization()(model)
    model = layers.Activation("relu")(model)
    model = layers.MaxPooling2D((2, 2))(model)

    model = layers.Conv2D(64, (3, 3))(model)
    model = layers.BatchNormalization()(model)
    model = layers.Activation("relu")(model)
    model = layers.MaxPooling2D((2, 2))(model)

    model = layers.Flatten()(model)
    return model


def create_late_fusion_model(channels=3, img_height=584, img_width=480):
    input_shape = (img_height, img_width, channels)

    before_input = layers.Input(shape=input_shape)
    before_model = create_conv_layer(before_input, input_shape)

    after_input = layers.Input(shape=input_shape)
    after_model = create_conv_layer(after_input, input_shape)

    conv = layers.concatenate([before_model, after_model])
    conv = layers.Flatten()(conv)

    dense = layers.Dense(128, activation='relu')(conv)
    dense = layers.Dropout(0.25)(dense)
    dense = layers.Dense(128, activation='relu')(dense)
    dense = layers.Dropout(0.25)(dense)

    output = layers.Dense(2, activation='softmax')(dense)

    return Model(inputs=[before_input, after_input], outputs=[output])


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
        if area > 10:
            x, y, w, h = cv2.boundingRect(c)
            before_region[y:y + h, x:x + w] = before[y:y + h, x:x + w]
            after_region[y:y + h, x:x + w] = after[y:y + h, x:x + w]

    return before_region, after_region

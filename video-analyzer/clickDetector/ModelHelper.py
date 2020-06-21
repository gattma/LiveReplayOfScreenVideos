from tensorflow.keras import layers
from tensorflow.keras.models import Model

NUM_CLASSES = 2


def create_conv_layers_VGG(input_img, input_shape):
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


def create_late_fusion_model_VGG(channels=3, img_height=584, img_width=480):
    input_shape = (img_height, img_width, channels)

    before_input = layers.Input(shape=input_shape)
    before_model = create_conv_layers_VGG(before_input, input_shape)

    after_input = layers.Input(shape=input_shape)
    after_model = create_conv_layers_VGG(after_input, input_shape)

    conv = layers.concatenate([before_model, after_model])
    conv = layers.Flatten()(conv)

    dense = layers.Dense(128, activation='relu')(conv)
    dense = layers.Dropout(0.25)(dense)
    dense = layers.Dense(128, activation='relu')(dense)
    dense = layers.Dropout(0.25)(dense)

    output = layers.Dense(2, activation='softmax')(dense)

    return Model(inputs=[before_input, after_input], outputs=[output])

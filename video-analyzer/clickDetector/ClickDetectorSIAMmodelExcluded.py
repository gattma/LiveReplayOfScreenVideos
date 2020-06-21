import clickDetector.ModelHelper as modelHelper
from clickDetector.MultipleInputDatagenerator import MultipleInputDatagenerator
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from clickDetector.ClickDetectorUtil import count_files_in_dir
from enum import Enum


VALIDATION_SPLIT = 0.2


class NetworkArchitecture(Enum):
    DEFAULT = 1
    VGG = 2


def load_model(func):
    def _load_model(self, *args, **kwargs):
        if self.model is None:
            print("initializing model...")
            self.model = modelHelper.create_late_fusion_model_VGG(self.channels, self.img_height, self.img_width)

        if self.weights_path is not None and self.weights_loaded is False:  # prediction mode
            self.load_weights(self.weights_path)

        return func(self, *args, **kwargs)
    return _load_model


class ClickDetector:
    weights_loaded = False

    def __init__(self, weights_path=None, channels=3, img_height=292, img_width=240, optimizer=optimizers.Adam()):
        self.model = None
        self.channels = channels
        self.img_height = img_height
        self.img_width = img_width
        self.optimizer = optimizer
        if weights_path is not None:  # prediction mode
            self.weights_path = weights_path

    @property
    @load_model
    def summary(self):
        return self.model.summary()

    @property
    @load_model
    def input_height(self):
        return self.model.layers[0].input_shape[0][1]

    @property
    @load_model
    def input_width(self):
        return self.model.layers[0].input_shape[0][2]

    @property
    @load_model
    def input_size(self):
        return self.input_width, self.input_height

    def load_weights(self, weights_path):
        print("loading weights from {}".format(weights_path))
        self.model.load_weights(weights_path)
        self.model.compile(loss='categorical_crossentropy', optimizer=self.optimizer,
                           metrics=['categorical_accuracy', 'accuracy'])
        self.weights_loaded = True

    @load_model
    def predict(self, before_frame, after_frame):
        if self.weights_loaded is not True:
            raise Exception("please specify and load trained weights")

        result = self.model.predict([before_frame, after_frame])
        if result[0][0] >= 0.7:
            return True  # CLICK
        else:
            return False

    @load_model
    def train(self, callbacks, dataset_dir, batch_size=8, epochs=10):
        self.model.compile(loss='categorical_crossentropy', optimizer=self.optimizer,
                           metrics=['categorical_accuracy', 'accuracy'])

        imgDataGenerator = ImageDataGenerator(
            rescale=1,  # 1./255,
            rotation_range=0,
            width_shift_range=0,
            height_shift_range=0,
            shear_range=0,
            zoom_range=0,
            horizontal_flip=False,
            vertical_flip=False,
            # fill_mode='nearest'
            validation_split=VALIDATION_SPLIT
        )

        generator = MultipleInputDatagenerator()
        before_dir = f"{dataset_dir}/before"
        after_dir = f"{dataset_dir}/after"
        train_generator = generator.flow_from_directory(
            generator=imgDataGenerator,
            before_dir=before_dir,
            after_dir=after_dir,
            batch_size=batch_size,
            subset="training"
        )

        validation_generator = generator.flow_from_directory(
            generator=imgDataGenerator,
            before_dir=before_dir,
            after_dir=after_dir,
            batch_size=batch_size,
            subset="validation"
        )

        nr_samples = count_files_in_dir(f"{before_dir}/click/") + count_files_in_dir(f"{before_dir}/no_click/")

        print(f"NR of train samples: {nr_samples * (1 - VALIDATION_SPLIT)}")
        print(f"NR of test samples : {nr_samples * VALIDATION_SPLIT}")

        history = self.model.fit_generator(
            train_generator,
            steps_per_epoch=nr_samples * (1 - VALIDATION_SPLIT) / batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=nr_samples * VALIDATION_SPLIT / batch_size,
            # use_multiprocessing=True,
            shuffle=False,
            verbose=1,
            callbacks=callbacks)

        return history

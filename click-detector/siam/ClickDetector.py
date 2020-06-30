from siam.MultipleInputDataGenerator import MultipleInputDataGenerator
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from siam.ClickDetectorUtil import count_files_in_dir, create_late_fusion_model
from tensorflow.keras.losses import CategoricalCrossentropy

ACC_LIMIT = 0.7
VALIDATION_SPLIT = 0.2


def load_model(func):
    def _load_model(self, *args, **kwargs):
        if self.model is None:
            print("initializing model...")
            self.model = create_late_fusion_model(self.channels, self.img_height, self.img_width)

        if self.weights_path is not None and self.weights_loaded is False:  # prediction mode
            self.load_weights(self.weights_path)

        return func(self, *args, **kwargs)
    return _load_model


class ClickDetector:
    weights_loaded = False

    def __init__(self, weights_path=None, channels=3, img_height=292, img_width=240,
                 optimizer=optimizers.Adam(), loss=CategoricalCrossentropy(),
                 metrics=None):
        if metrics is None:
            metrics = ['categorical_accuracy', 'accuracy']

        self.model = None
        self.channels = channels
        self.img_height = img_height
        self.img_width = img_width
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
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
        self.model.compile(loss=self.loss, optimizer=self.optimizer, metrics=self.metrics)
        self.weights_loaded = True

    @load_model
    def predict(self, before_frame, after_frame):
        if self.weights_loaded is not True:
            raise Exception("please specify and load trained weights")

        result = self.model.predict([before_frame, after_frame])
        if result[0][0] >= ACC_LIMIT:
            return True  # CLICK
        else:
            return False

    # TODO überarbeiten
    def train(self, callbacks, dataset_dir, batch_size=8, epochs=10):

        imgDataGenerator = ImageDataGenerator(
            rescale=1,  # 1./255,
            rotation_range=0,
            width_shift_range=0,
            height_shift_range=0,
            shear_range=0,
            zoom_range=0,
            horizontal_flip=False,
            vertical_flip=False,
            validation_split=VALIDATION_SPLIT
        )

        generator = MultipleInputDataGenerator()
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

        self.model = create_late_fusion_model(self.channels, self.img_height, self.img_width)
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

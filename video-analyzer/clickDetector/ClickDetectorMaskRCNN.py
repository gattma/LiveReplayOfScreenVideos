from clickDetector.mrcnn.config import Config
from clickDetector.mrcnn import model as modellib


class InferenceConfig(Config):

    # Give the configuration a recognizable name
    NAME = "cursor"

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    NUM_CLASSES = 1 + 1  # Background + cursor and cursor_click

    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


class ClickDetector:

    def __init__(self, weights_path, model_dir=None, debug=False):
        config = InferenceConfig()
        self.debug = debug
        if debug:
            config.display()

        self.model = modellib.MaskRCNN(mode="inference", config=config, model_dir=model_dir)
        self.model.load_weights(weights_path, by_name=True)

    def detect(self, image):
        r = self.model.detect([image], verbose=0)[0]
        rois = r['rois']

        if len(rois) != 0 and r['scores'][0] > 0.99:
            y1 = rois[0][0]
            x1 = rois[0][1]
            y2 = rois[0][2]
            x2 = rois[0][3]
            if self.debug:
                print("Found click at ({},{}) and ({},{})".format(x1, y1, x2, y2))

            return True, x1, y1, x2, y2, r['scores'][0]
        else:
            return False, -1, -1, -1, -1, 0

    def detect_detailed(self, image):
        return self.model.detect([image], verbose=0)[0]

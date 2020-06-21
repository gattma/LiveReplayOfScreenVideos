from Configuration import Configuration
from util.Constants import Constants
from analyzer.VideoAnalyzerMaskRCNN import VideoAnalyzer as VideoAnalyzerMaskRCNN
from analyzer.VideoAnalyzerSIAM import VideoAnalyzer as VideoAnalyzerSIAM
from clickDetector.ClickDetectorMaskRCNN import ClickDetector as ClickDetectorMaskRCNN
from clickDetector.ClickDetectorSIAMmodelExcluded import ClickDetector as ClickDetectorSIAM


def build_mask_rcnn_analyzer(config: Configuration):
    return VideoAnalyzerMaskRCNN(
        ClickDetectorMaskRCNN(config.mask_rcnn_weights, debug=config.debug),
        config.debug
    )


def build_siamese_nn_analyzer(config: Configuration):
    return VideoAnalyzerSIAM(
        ClickDetectorSIAM(config.siamese_nn_weights),
        debug=config.debug
    )


def build_analyzer(config: Configuration):
    if config.active_solution == Constants.DETECTOR_SOLUTION_MASK:
        return build_mask_rcnn_analyzer(config)
    else:
        return build_siamese_nn_analyzer(config)

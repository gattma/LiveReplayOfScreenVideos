import configparser
from util.Constants import Constants


class Configuration:

    def __init__(self, config_file="configuration.ini"):
        self.parser = configparser.ConfigParser()
        self.parser.read(config_file)
        self.config_file = config_file
        self._dirty = True

    @property
    def dirty(self):
        return self._dirty

    @dirty.setter
    def dirty(self, value):
        self._dirty = value

    @property
    def valid(self):
        if self.active_solution == Constants.DETECTOR_SOLUTION_SIAM and \
                self.siamese_nn_weights != Constants.NOT_VALID:
            return True
        elif self.active_solution == Constants.DETECTOR_SOLUTION_MASK and \
                self.mask_rcnn_weights != Constants.NOT_VALID:
            return True
        else:
            return False

    @property
    def siamese_nn_weights(self):
        return self.parser.get(Constants.ConfigKeys.SEC_SIAMESE, Constants.ConfigKeys.WEIGHTS)

    @siamese_nn_weights.setter
    def siamese_nn_weights(self, value):
        self.parser.set(Constants.ConfigKeys.SEC_SIAMESE, Constants.ConfigKeys.WEIGHTS, value)
        self._persist_()

    @property
    def mask_rcnn_weights(self):
        return self.parser.get(Constants.ConfigKeys.SEC_MASK, Constants.ConfigKeys.WEIGHTS)

    @mask_rcnn_weights.setter
    def mask_rcnn_weights(self, value):
        self.parser.set(Constants.ConfigKeys.SEC_MASK, Constants.ConfigKeys.WEIGHTS, value)
        self._persist_()

    @property
    def debug(self):
        return self.parser.get(Constants.ConfigKeys.SEC_PREFERENCES, Constants.ConfigKeys.DEBUG)

    @debug.setter
    def debug(self, value):
        self.parser.set(Constants.ConfigKeys.SEC_PREFERENCES, Constants.ConfigKeys.DEBUG, str(value))
        self._persist_()

    @property
    def active_solution(self):
        return self.parser.get(Constants.ConfigKeys.SEC_PREFERENCES, Constants.ConfigKeys.ACTIVE)

    @active_solution.setter
    def active_solution(self, value):
        self.parser.set(Constants.ConfigKeys.SEC_PREFERENCES, Constants.ConfigKeys.ACTIVE, value)
        self._persist_()

    def _persist_(self):
        with open(self.config_file, 'w') as configfile:
            self.parser.write(configfile)
        self._dirty = True

    def as_string(self):
        return f"Configuration(debug={self.debug}, active-analyzer={self.active_solution}, " \
               f"active-weights={self.mask_rcnn_weights if self.active_solution == Constants.DETECTOR_SOLUTION_MASK else self.siamese_nn_weights})"

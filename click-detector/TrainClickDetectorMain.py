from getopt import getopt, GetoptError
from util.Constants import Constants
from util.Helper import save_to_int
from siam.ClickDetector import ClickDetector as ClickDetectorSiam

import sys

DEFAULT_CONFIG = {Constants.ConfigKeys.SOLUTION: 1, Constants.ConfigKeys.DATADIR: ""}


def parse_cli_params(argv):
    try:
        opts, args = getopt(argv, "s:t", ["solution=", "traindatadir="])
    except GetoptError:
        print_help()
        sys.exit(2)

    train_config = DEFAULT_CONFIG
    for opt, arg in opts:
        if opt == "-h":
            print_help()
            sys.exit()
        elif opt in ('-s', '--solution'):
            if save_to_int(arg) in (Constants.SOLUTION_SIAM_NN, Constants.SOLUTION_MASK_RCNN):
                train_config[Constants.ConfigKeys.SOLUTION] = int(arg)
            else:
                print(f"WARNING: Only values '1' and '2' are allowed for param '-s'. Actual value was '{arg}'. "
                      f"Using default '{train_config[Constants.ConfigKeys.SOLUTION]}'")

        elif opt in ('-t', '--traindatadir'):
            train_config[Constants.ConfigKeys.DATADIR] = arg

    print(f"Actual configuration: {train_config}")
    return train_config


def train_network(config):
    # TODO
    print(config)
    if config[Constants.ConfigKeys.SOLUTION] == Constants.SOLUTION_SIAM_NN:
        train_siam(config)
    elif config[Constants.ConfigKeys.SOLUTION] == Constants.SOLUTION_MASK_RCNN:
        train_mask_rcnn(config)
    else:
        print(f"WARNING: '{config[Constants.ConfigKeys.SOLUTION]} is not a valid solution!'")

def train_siam(config):
    print(f"train new siamese nn with config {config}")
    detector = ClickDetectorSiam()
    callbacks = None # Todo
    history = detector.train(callbacks=callbacks, dataset_dir=config[Constants.ConfigKeys.DATADIR])
    # TODO print history

def train_mask_rcnn(config):
    print(f"train new mask rcnn with config {config}")
    # TODO
    pass


def print_help():
    print('TrainClickDetectorMain.py [-s <SOLUTION>] [-t <TRAINDATADIR>] -h')
    print(f'  -s <SOLUTION>: 1 for Siamese NN, 2 for Mask R-CNN => DEFAULT: {DEFAULT_CONFIG["solution"]}')
    print(f'  -t <TRAINDATADIR>: Path to traindata => DEFAULT: {DEFAULT_CONFIG["datadir"]}')
    print('  -h: Show Help')


if __name__ == '__main__':
    config = parse_cli_params(sys.argv[1:])
    train_network(config)

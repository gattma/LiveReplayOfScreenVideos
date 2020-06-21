class Constants:

    NOT_VALID = "[NOT VALID]"
    DETECTOR_SOLUTION_MASK = "MASK R-CNN"
    DETECTOR_SOLUTION_SIAM = "Siamese NN"
    TXT_EMPTY = ""

    class ConfigKeys:
        DEBUG = "debug"
        WEIGHTS = "weights"
        ACTIVE = "active"

        SEC_PREFERENCES = "Preferences"
        SEC_SIAMESE = "SiameseNN"
        SEC_MASK = "MaskRCNN"

    class Main:
        TITLE = "Video Analyzer"
        TXT_EXIT = "Exit"
        TXT_LOAD = "Load video"
        TXT_ANALYZE = "Analyze"
        TXT_PREFERENCES = "Preferences"

        SHORTCUT_EXIT = "Ctrl+Q"
        SHORTCUT_LOAD = "Ctrl+L"
        SHORTCUT_ANALYZE = "Ctrl+A"
        SHORTCUT_PREFERENCES = "Ctrl+P"

    class Settings:
        TXT_SETTINGS = "Settings"
        TXT_DEBUG = "Debug:"
        TXT_SIAM_WEIGHTS = "SIAM Weights:"
        TXT_MASK_WEIGHTS = "MASK Weights:"
        TXT_SOLUTION = "Select solution:"
        BTN_SIAM_WEIGHTS = "Choose SIAM weights"
        BTN_MASK_WEIGHTS = "Choose MASK weights"
        AKTIV = "True"

    class Result:
        TITLE = "Result"
        BTN_REMOVE = "Remove"
        BTN_SELECT = "Select new"
        TOOLBAR_SAVE = "Save"
        TOOLBAR_OPEN_BROWSER = "Open in Browser"
        TOOLBAR_EXPORT_HTML = "Export HTML"
        TOOLBAR_EXPORT_FRAMES = "Export Full Frames"
        SHORTCUT_SAVE = "Ctrl+S"
        SHORTCUT_OPEN_BROWSER = "Ctrl+O"
        TXT_SELECT_DIR = "Select Directory"

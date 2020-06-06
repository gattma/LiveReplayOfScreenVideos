package at.gattma.fh.masterthesis.util;

import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyCodeCombination;
import javafx.scene.input.KeyCombination;
import javafx.stage.FileChooser;

public class Constants {

    public static final String OPEN_VIDEO_TITLE = "Play video file";
    public static final String OPEN_REPLAY_TITLE = "Play .replay file";
    public static final String OPEN_VIDEO_REPLAY_TITLE = "Play video and replay";

    public static final KeyCombination CTR_P_COMB = new KeyCodeCombination(KeyCode.P, KeyCombination.CONTROL_DOWN);

    public static final FileChooser.ExtensionFilter VIDEO_FILE_EXT
            = new FileChooser.ExtensionFilter("VIDEO files", "*.avi", "*.mp4");
    public static final FileChooser.ExtensionFilter REPLAY_FILE_EXT
            = new FileChooser.ExtensionFilter("REPLAY files", "*.replay");

    public static final String ICON_SIZE = "8px";

    public static final class WINDOW {

        public static final int WIDTH = 600;
        public static final int HEIGHT = 600;
        public static final String TITLE = "Model Player";

    }

    public static final class ELEMENTS {

        public static final String BTN_OPEN_VIDEO_TXT = "open video";
        public static final String BTN_PAUSE_TXT = "pause";
        public static final String BTN_PLAY_TXT = "play";
        public static final String BTN_STOP_TXT = "stop";

        public static final String BTN_OPEN_MODEL_TXT = "open model";
        public static final String BTN_PLAY_MODEL_TXT = "play model";

    }
}

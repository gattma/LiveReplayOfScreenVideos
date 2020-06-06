package at.gattma.fh.masterthesis.components;

import at.gattma.fh.masterthesis.util.Constants;
import at.gattma.fh.masterthesis.player.AbstractPlayer;
import de.jensd.fx.fontawesome.AwesomeDude;
import de.jensd.fx.fontawesome.AwesomeIcon;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.Slider;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;

public class MediaBar extends HBox {

    private Slider time;
    private Slider speed;
    private AbstractPlayer player;
    private PlayButton playButton;
    private CheckBox ignoreDelay;

    public MediaBar(AbstractPlayer player, MediaBarBuilder builder) {
        this.player = player;
        setAlignment(Pos.CENTER_LEFT);
        setPadding(new Insets(5, 10, 5, 10));

        if (builder.generatePlayBtn()) {
            playButton = new PlayButton(player);
            setMargin(playButton, new Insets(0, 10, 0, 0));
            AwesomeDude.setIcon(playButton, AwesomeIcon.PLAY, Constants.ICON_SIZE);
            getChildren().add(playButton);
            this.player.onEndOfSource(() -> AwesomeDude.setIcon(playButton, AwesomeIcon.REPEAT, Constants.ICON_SIZE));
        }

        if (builder.generateTimeSlider()) {
            time = new Slider();
            HBox.setHgrow(time, Priority.ALWAYS);
            getChildren().add(time);
            time.valueProperty().addListener(ov -> {
                if (time.isPressed()) {
                    this.player.seek(time.getValue() / 100);
                }
            });
        }

        if (builder.generateSpeedSlider()) {
            speed = new SpeedSlider(player);
            getChildren().add(new Label("Speed: "));
            getChildren().add(speed);
        }

        if (builder.generateIgnoreDelayCbx()) {
            ignoreDelay = new CheckBox("Ignore Delay");
            getChildren().add(ignoreDelay);
        }

        this.player.addCurrentTimeListener(ov -> updatesValues());
    }

    private void updatesValues() {
        Platform.runLater(() -> time.setValue((player.getCurrentTime().toMillis() / player.getTotalDuration().toMillis()) * 100));
    }

    public double getSpeed() {
        return this.speed == null ? 1.0 : this.speed.getValue();
    }

    public void updatePlayBtnIcon(AwesomeIcon icon) {
        Platform.runLater(() -> this.playButton.updateIcon(icon));
    }

    public boolean ignoreDelay() {
        return ignoreDelay != null && ignoreDelay.isSelected();
    }

    public static MediaBarBuilder builder() {
        return new MediaBarBuilder();
    }

    public static class MediaBarBuilder {
        private boolean playBtn;
        private boolean timeSlider;
        private boolean speedSlider;
        private boolean ignoreDelayCbx;

        private MediaBarBuilder() {
            this.playBtn = true;
            this.timeSlider = false;
            this.speedSlider = false;
            this.ignoreDelayCbx = false;
        }

        public MediaBarBuilder playBtn(boolean playBtn) {
            this.playBtn = playBtn;
            return this;
        }

        public boolean generatePlayBtn() {
            return this.playBtn;
        }

        public MediaBarBuilder timeSlider(boolean timeSlider) {
            this.timeSlider = timeSlider;
            return this;
        }

        public boolean generateTimeSlider() {
            return this.timeSlider;
        }

        public MediaBarBuilder speedSlider(boolean speedSlider) {
            this.speedSlider = speedSlider;
            return this;
        }

        public boolean generateSpeedSlider() {
            return this.speedSlider;
        }

        public MediaBarBuilder ignoreDelayCbx(boolean ignoreDelayCbx) {
            this.ignoreDelayCbx = ignoreDelayCbx;
            return this;
        }

        public boolean generateIgnoreDelayCbx() {
            return this.ignoreDelayCbx;
        }
    }
}
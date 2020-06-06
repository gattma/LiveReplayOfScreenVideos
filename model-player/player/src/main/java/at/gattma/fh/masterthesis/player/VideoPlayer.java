package at.gattma.fh.masterthesis.player;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.actions.ClickAction;
import at.gattma.fh.masterthesis.exceptions.ParseModelException;
import at.gattma.fh.masterthesis.components.Card;
import at.gattma.fh.masterthesis.components.MediaBar;
import at.gattma.fh.masterthesis.util.ArchiveHelper;
import javafx.beans.InvalidationListener;
import javafx.scene.control.TitledPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.util.Duration;

import java.io.File;
import java.net.MalformedURLException;
import java.util.List;


public class VideoPlayer extends AbstractPlayer {
    private final MediaPlayer player;
    private final MediaBar mediaBar;
    private List<Action> workflow;

    public VideoPlayer(File videoFile) throws MalformedURLException, ParseModelException {

        Media media = new Media(videoFile.toURI().toURL().toExternalForm());
        player = new MediaPlayer(media);
        MediaView view = new MediaView(player);

        Pane mpane = new Pane();
        mpane.getChildren().add(view);
        setCenter(mpane);

        VBox actions = new VBox();
        workflow = ArchiveHelper.createWorkflow(ArchiveHelper.findReplayFileInDir(videoFile));
        int actionNr = 0;
        for (int i = 0; i < workflow.size(); i++) {
            Action a = workflow.get(i);
            if (a instanceof ClickAction) {
                ClickAction action = (ClickAction) a;
                TitledPane pane = new TitledPane(
                        String.format("CLICK-ACTION (%d)", actionNr),
                        new Card(action.getImgPath(), "CLICK", this, i));
                pane.setExpanded(false);
                actions.getChildren().add(pane);
                actionNr++;
            }
        }

        setRight(actions);

        mediaBar = new MediaBar(
                this,
                MediaBar.builder().speedSlider(true).timeSlider(true)
        );
        setBottom(mediaBar);
    }

    @Override
    public void play(int actionIdx) {
        Action action = this.workflow.get(actionIdx);
        if (action instanceof ClickAction) {
            float timestamp = ((ClickAction) action).getTimestamp();
            this.seek(timestamp / 10000);
        }
    }

    @Override
    protected void onPlay() {
        this.player.play();
    }

    @Override
    protected void onPause() {
        if (this.player != null) player.pause();
    }

    public MediaPlayer.Status getStatus() {
        return this.player.getStatus();
    }

    public Duration getCurrentTime() {
        return this.player.getCurrentTime();
    }

    public Duration getTotalDuration() {
        return this.player.getTotalDuration();
    }

    public void seekToStartTime() {
        this.player.seek(this.player.getStartTime());
    }

    public void seek(double seek) {
        this.player.seek(this.player.getMedia().getDuration().multiply(seek));
    }

    public void setRate(double rate) {
        this.player.setRate(rate);
    }

    public void addCurrentTimeListener(InvalidationListener listener) {
        this.player.currentTimeProperty().addListener(listener);
    }

    public void onEndOfSource(Runnable runnable) {
        this.player.setOnEndOfMedia(runnable);
    }

    public void setOnReady(Runnable runnable) {
        if (this.player != null) this.player.setOnReady(runnable);
    }

    @Override
    protected MediaBar getMediaBar() {
        return this.mediaBar;
    }

    @Override
    public void updateStatus(MediaPlayer.Status newStatus) {
        // NOT USED HERE
    }

    @Override
    public void onFinished() {
        // NOT USED HERE
    }

}

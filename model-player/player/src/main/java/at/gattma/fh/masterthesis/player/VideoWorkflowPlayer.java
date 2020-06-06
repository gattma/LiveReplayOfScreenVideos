package at.gattma.fh.masterthesis.player;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.exceptions.ParseModelException;
import at.gattma.fh.masterthesis.components.MediaBar;
import at.gattma.fh.masterthesis.tasks.RunWorkflowTask;
import at.gattma.fh.masterthesis.util.ArchiveHelper;
import javafx.beans.InvalidationListener;
import javafx.scene.layout.Pane;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import javafx.scene.media.MediaView;
import javafx.util.Duration;

import java.io.File;
import java.net.MalformedURLException;
import java.util.List;

public class VideoWorkflowPlayer extends AbstractPlayer {

    private final MediaPlayer player;
    private final MediaBar mediaBar;
    private List<Action> workflow;
    private RunWorkflowTask runWorkflowTask;

    public VideoWorkflowPlayer(File videoFile) throws ParseModelException, MalformedURLException {
        Media media = new Media(videoFile.toURI().toURL().toExternalForm());
        player = new MediaPlayer(media);
        MediaView view = new MediaView(player);
        Pane mpane = new Pane();
        mpane.getChildren().add(view);
        setCenter(mpane);

        workflow = ArchiveHelper.createWorkflow(ArchiveHelper.findReplayFileInDir(videoFile));

        mediaBar = new MediaBar(
                this,
                MediaBar.builder().speedSlider(true).timeSlider(true)
        );
        setBottom(mediaBar);
    }

    @Override
    public void play(int actionIdx) {
        // NOT USED HERE
    }

    @Override
    protected void onPlay() {
        this.player.play();
        if (player.getStatus() == MediaPlayer.Status.READY || player.getStatus() == MediaPlayer.Status.STOPPED) {
            this.runWorkflowTask = new RunWorkflowTask(
                    this.workflow,
                    false,
                    this.workflow.size(),
                    this
            );
            this.runWorkflowTask.start();
        } else if (player.getStatus() == MediaPlayer.Status.PAUSED) {
            this.runWorkflowTask.resume();
        }
    }

    @Override
    protected void onPause() {
        if (this.player != null) player.pause();
        if (this.runWorkflowTask != null) this.runWorkflowTask.suspend();
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

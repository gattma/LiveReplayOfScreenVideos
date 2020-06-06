package at.gattma.fh.masterthesis.player;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.actions.ClickAction;
import at.gattma.fh.masterthesis.exceptions.ParseModelException;
import at.gattma.fh.masterthesis.components.Card;
import at.gattma.fh.masterthesis.components.MediaBar;
import at.gattma.fh.masterthesis.tasks.RunWorkflowTask;
import at.gattma.fh.masterthesis.util.ArchiveHelper;
import de.jensd.fx.fontawesome.AwesomeIcon;
import javafx.beans.InvalidationListener;
import javafx.scene.control.TitledPane;
import javafx.scene.layout.VBox;
import javafx.scene.media.MediaPlayer;
import javafx.util.Duration;

import java.io.File;
import java.util.List;

public class WorkflowPlayer extends AbstractPlayer {

    private final MediaBar mediaBar;
    private List<Action> workflow;
    private MediaPlayer.Status status;
    private RunWorkflowTask runWorkflowTask;

    public WorkflowPlayer(File replayFile) throws ParseModelException {
        workflow = ArchiveHelper.createWorkflow(replayFile);

        VBox actions = new VBox();
        int actionNr = 0;
        for(int i = 0; i < workflow.size();i++) {
            Action a  = workflow.get(i);
            if(a instanceof ClickAction) {
                ClickAction action = (ClickAction) a;
                TitledPane pane = new TitledPane(
                        String.format("CLICK-ACTION (%d)", actionNr),
                        new Card(action.getImgPath(), "CLICK", this, i));
                pane.setExpanded(false);
                actions.getChildren().add(pane);
                actionNr++;
            }
        }
        setCenter(actions);

        mediaBar = new MediaBar(
                this,
                MediaBar.builder().speedSlider(false).ignoreDelayCbx(true)
        );
        setBottom(mediaBar);
        status = MediaPlayer.Status.READY;
    }

    public void play(int actionIdx) {
        if (this.status == MediaPlayer.Status.READY || this.status == MediaPlayer.Status.STOPPED) {
            this.runWorkflowTask = new RunWorkflowTask(this.workflow, mediaBar.ignoreDelay(), actionIdx, this);
            this.runWorkflowTask.start();
        } else if (this.status == MediaPlayer.Status.PAUSED) {
            this.runWorkflowTask.resume(actionIdx);
        }
    }

    @Override
    protected void onPlay() {
        if (this.status == MediaPlayer.Status.READY || this.status == MediaPlayer.Status.STOPPED) {
            runWorkflowTask = new RunWorkflowTask(this.workflow, mediaBar.ignoreDelay(), workflow.size(), this);
            this.runWorkflowTask.start();
            this.status = MediaPlayer.Status.PLAYING;
        } else if (this.status == MediaPlayer.Status.PAUSED) {
            this.runWorkflowTask.resume();
            this.status = MediaPlayer.Status.PLAYING;
        }
    }

    @Override
    protected void onPause() {
        this.status = MediaPlayer.Status.PAUSED;
        if(this.runWorkflowTask != null) this.runWorkflowTask.suspend();
    }

    public void onFinished() {
        this.mediaBar.updatePlayBtnIcon(AwesomeIcon.PLAY);
        this.status = MediaPlayer.Status.STOPPED;
    }

    public MediaPlayer.Status getStatus() {
        return this.status;
    }

    @Override
    protected MediaBar getMediaBar() {
        return this.mediaBar;
    }

    @Override
    public void updateStatus(MediaPlayer.Status newStatus) {
        this.status = newStatus;
    }

    //<editor-fold desc="UNSUPPORTED METHODS"
    public Duration getCurrentTime() {
        throw new UnsupportedOperationException();
    }

    public Duration getTotalDuration() {
        throw new UnsupportedOperationException();
    }

    public void seekToStartTime() {
        // IGNORE
    }

    public void seek(double seek) {
        // IGNORE
    }

    public void setRate(double rate) {
        // IGNORE
    }

    public void addCurrentTimeListener(InvalidationListener listener) {
        // IGNORE
    }

    public void onEndOfSource(Runnable runnable) {
        // IGNORE
    }

    public void setOnReady(Runnable runnable) {
        // IGNORE
    }
    //</editor-fold>

}

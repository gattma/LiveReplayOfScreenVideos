package at.gattma.fh.masterthesis.tasks;

import at.gattma.fh.masterthesis.actions.Action;
import at.gattma.fh.masterthesis.actions.DelayAction;
import at.gattma.fh.masterthesis.player.AbstractPlayer;
import at.gattma.fh.masterthesis.util.MessageUtil;
import javafx.application.Platform;
import javafx.scene.control.Alert;
import javafx.scene.media.MediaPlayer;
import org.sikuli.script.Screen;

import java.util.List;
import java.util.stream.Collectors;

public class RunWorkflowTask implements Runnable {

    private List<Action> workflow;
    private boolean ignoreDelay;
    private int runToIdx;
    private AbstractPlayer player;

    private boolean suspend = false;

    public RunWorkflowTask(List<Action> workflow,
                           boolean ignoreDelay,
                           int runToIdx,
                           AbstractPlayer player) {
        this.workflow = workflow;
        this.ignoreDelay = ignoreDelay;
        this.runToIdx = runToIdx;
        this.player = player;
    }

    public void start() {
        new Thread(this).start();
    }

    @Override
    public void run() {
        playWorkflow(workflow, ignoreDelay);
    }

    public synchronized void suspend() {
        suspend = true;
    }

    public synchronized void resume() {
        suspend = false;
        notify();
    }

    public synchronized void resume(int newIdx) {
        if(newIdx > this.runToIdx) {
            this.runToIdx = newIdx;
        }
        resume();
    }

    private void playWorkflow(List<Action> workflow, boolean ignoreDelay) {
        Screen screen = new Screen();
        List<Action> w = ignoreDelay ? filterDelayActions(workflow) : workflow;

        try {
            this.player.updateStatus(MediaPlayer.Status.PLAYING);
            for(int i = 0; i < w.size(); i++) {
                w.get(i).execute(screen);
                synchronized (this) {
                    if(suspend || i == runToIdx) {
                        this.player.updateStatus(MediaPlayer.Status.PAUSED);
                        wait();
                        this.player.updateStatus(MediaPlayer.Status.PLAYING);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Not able to play workflow, " + e.getMessage());
            MessageUtil.showErrorMessage(
                    "Replaying Error",
                    "Error happen when replaying model",
                    "Cannot replay the model, " + e.getMessage()
            );
        }

        this.player.onFinished();
    }

    private List<Action> filterDelayActions(List<Action> workflow) {
        return workflow.stream().filter(a -> !(a instanceof DelayAction)).collect(Collectors.toList());
    }
}

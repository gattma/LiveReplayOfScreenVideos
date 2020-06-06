package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.exceptions.ActionFailedException;
import org.sikuli.script.Screen;

public class DelayAction implements Action {

    private double delayInMillis;

    public DelayAction(double delayInMillis) {
        this.delayInMillis = delayInMillis;
    }

    @Override
    public void execute(Screen screen) throws ActionFailedException {
        try {
            Thread.sleep(Math.round(delayInMillis));
        } catch (InterruptedException e) {
            // IGNORE
        }
    }

    public void updateFactor(double delayFactor) {
        this.delayInMillis /= delayFactor;
    }

    public double getDelayInMillis() {
        return this.delayInMillis;
    }
}

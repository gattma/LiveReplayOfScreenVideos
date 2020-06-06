package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.exceptions.ActionFailedException;
import at.gattma.fh.masterthesis.util.Constants;
import org.sikuli.script.FindFailed;
import org.sikuli.script.Pattern;
import org.sikuli.script.Screen;

public class ClickAction implements Action {

    private Pattern action;
    private float timestamp;

    public ClickAction(String imagePath) {
        this.action = new Pattern(imagePath);
        this.timestamp = 0.0f;
    }

    public ClickAction(String imagePath, float timestamp) {
        this.action = new Pattern(imagePath);
        this.timestamp = timestamp;
    }

    public void execute(Screen screen) throws ActionFailedException {
        try {
            screen.wait(action.similar(Constants.PRECISION), Constants.TIMEOUT).click();
        } catch(FindFailed ffe) {
            throw new ActionFailedException(ffe);
        }
    }

    public String getImgPath() {
        return this.action.getFilename();
    }

    public float getTimestamp() {
        return this.timestamp;
    }

    public void setTimestamp(float timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "CLICK(" + this.action.getFilename() + ")";
    }
}

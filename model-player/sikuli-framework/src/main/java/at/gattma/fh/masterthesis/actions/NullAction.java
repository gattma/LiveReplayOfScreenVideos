package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.exceptions.ActionFailedException;
import org.sikuli.script.Screen;

public class NullAction implements Action {

    @Override
    public void execute(Screen screen) throws ActionFailedException {
        // Do nothing, see null value pattern
    }
}

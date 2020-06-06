package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.exceptions.ActionFailedException;
import org.sikuli.script.Screen;

public interface Action {

    void execute(Screen screen) throws ActionFailedException;

}

package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.exceptions.ActionFailedException;
import at.gattma.fh.masterthesis.util.KeyHelper;
import org.sikuli.script.Screen;

import java.util.Objects;

public class KeyPressAction implements Action {

    private int keyCode = -1;

    public KeyPressAction(String key) {
        Objects.requireNonNull(key);
        this.keyCode = KeyHelper.getKeyCode(key);
    }

    @Override
    public void execute(Screen screen) throws ActionFailedException {
        screen.keyDown(keyCode);
        screen.keyUp(keyCode);
    }
}

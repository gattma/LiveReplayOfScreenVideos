package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.exceptions.ActionFailedException;
import org.sikuli.script.Screen;

public class TypeAction implements Action {

    private String text;

    public TypeAction(String text) {
        this.text = text;
    }

    @Override
    public void execute(Screen screen) throws ActionFailedException {
        screen.paste(text);
        try{
            Thread.sleep(500);
        } catch (InterruptedException e) {}
    }
}

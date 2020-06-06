package at.gattma.fh.masterthesis.exceptions;

public class ActionFailedException extends Exception {
    public ActionFailedException() {
        super();
    }
    public ActionFailedException(String s) {
        super(s);
    }
    public ActionFailedException(String s, Throwable throwable) {
        super(s, throwable);
    }
    public ActionFailedException(Throwable throwable) {
        super(throwable);
    }
}

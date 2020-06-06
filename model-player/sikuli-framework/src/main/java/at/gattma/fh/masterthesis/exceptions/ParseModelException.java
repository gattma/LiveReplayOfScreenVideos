package at.gattma.fh.masterthesis.exceptions;

public class ParseModelException extends Exception {
    public ParseModelException() {
        super();
    }
    public ParseModelException(String s) {
        super(s);
    }
    public ParseModelException(String s, Throwable throwable) {
        super(s, throwable);
    }
    public ParseModelException(Throwable throwable) {
        super(throwable);
    }
}

package at.gattma.fh.masterthesis.util;

public class Constants {

    public static final float PRECISION = 0.8f;
    public static final int TIMEOUT = 5;

    public static class ACTION {
        private ACTION() {
        }

        public static final String CLICK    = "click";
        public static final String KEYPRESS = "keypress";
        public static final String TYPE     = "type";
        public static final String DELAY    = "delay";
    }

    public static class TAG {
        private TAG() {
        }

        public static final String ACTION       = "action";
        public static final String SETUP        = "setup";
        public static final String INTERACTION  = "interaction";
    }

    public static class ATTRIBUTE {
        private ATTRIBUTE() {
        }

        public static final String TYPE = "type";
        public static final String TIMESTAMP = "timestamp";
    }
}

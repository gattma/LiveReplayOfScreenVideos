package at.gattma.fh.masterthesis.util;

import org.sikuli.script.Key;

import java.util.Objects;

public class KeyHelper {

    private static final String SIKULI_KEY_FORMAT = "#%s.";

    public static int getKeyCode(String key) {
        Objects.requireNonNull(key);

        if(key.length() > 1) {
            return Key.toJavaKeyCodeFromText(String.format(SIKULI_KEY_FORMAT, key.toUpperCase()));
        } else {
            int[] codes = Key.toJavaKeyCode(key);
            return codes != null ? codes[0] : -1;
        }
    }
}

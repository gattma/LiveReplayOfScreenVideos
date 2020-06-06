package at.gattma.fh.masterthesis.actions;

import at.gattma.fh.masterthesis.util.Constants;
import org.w3c.dom.Element;

import java.util.Objects;

public class ActionFactory {

    public static Action buildAction(Element element, String val) {
        Objects.requireNonNull(element);
        String action = element.getAttribute(Constants.ATTRIBUTE.TYPE);

        switch (action.toLowerCase()) {
            case Constants.ACTION.CLICK:
                String timestamp = element.getAttribute(Constants.ATTRIBUTE.TIMESTAMP);
                if("".equalsIgnoreCase(timestamp)) {
                    return new ClickAction(val);
                } else {
                    return new ClickAction(val, Float.parseFloat(timestamp));
                }

            case Constants.ACTION.KEYPRESS:
                return new KeyPressAction(val);

            case Constants.ACTION.TYPE:
                return new TypeAction(val);

            case Constants.ACTION.DELAY:
                return new DelayAction(Double.parseDouble(val));

            default:
                return new NullAction();
        }
    }
}

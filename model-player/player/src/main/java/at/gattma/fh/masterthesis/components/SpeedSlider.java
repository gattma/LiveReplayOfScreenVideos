package at.gattma.fh.masterthesis.components;

import at.gattma.fh.masterthesis.player.AbstractPlayer;
import javafx.scene.control.Slider;

public class SpeedSlider extends Slider {

    public SpeedSlider(AbstractPlayer player) {
        setMin(0.1);
        setMax(2);
        setValue(1);
        setShowTickLabels(true);
        setShowTickMarks(true);
        setMajorTickUnit(0.5);
        setMinorTickCount(1);
        setBlockIncrement(0.5);

        valueProperty().addListener(ov -> {
            if (isPressed()) {
                player.setRate(getValue());
            }
        });
    }

}

package at.gattma.fh.masterthesis.components;

import at.gattma.fh.masterthesis.util.Constants;
import at.gattma.fh.masterthesis.player.AbstractPlayer;
import de.jensd.fx.fontawesome.AwesomeDude;
import de.jensd.fx.fontawesome.AwesomeIcon;
import javafx.scene.control.Button;
import javafx.scene.control.Tooltip;
import javafx.scene.media.MediaPlayer;

public class PlayButton extends Button {

    public PlayButton(AbstractPlayer player) {
        setPrefWidth(30);
        Tooltip tooltip = new Tooltip("Play/Pause (Ctrl + P)");
        Tooltip.install(this, tooltip);
        setOnAction(e -> {
            MediaPlayer.Status status = player.getStatus();
            if (status != null)
                switch (status) {
                    case PLAYING:
                        if (player.getCurrentTime().greaterThanOrEqualTo(player.getTotalDuration())) {
                            player.seekToStartTime();
                            player.play();
                            AwesomeDude.setIcon(this, AwesomeIcon.PAUSE, Constants.ICON_SIZE);
                        } else {
                            player.pause();
                            AwesomeDude.setIcon(this, AwesomeIcon.PLAY, Constants.ICON_SIZE);
                            break;
                        }

                    case READY:
                    case HALTED:
                    case STOPPED:
                    case PAUSED:
                        player.play();
                        AwesomeDude.setIcon(this, AwesomeIcon.PAUSE, Constants.ICON_SIZE);
                        break;
                }
        });
    }

    public void updateIcon(AwesomeIcon icon) {
        AwesomeDude.setIcon(this, icon, Constants.ICON_SIZE);
    }

}

package at.gattma.fh.masterthesis.player;

import at.gattma.fh.masterthesis.components.MediaBar;
import de.jensd.fx.fontawesome.AwesomeIcon;
import javafx.beans.InvalidationListener;
import javafx.scene.layout.BorderPane;
import javafx.scene.media.MediaPlayer;
import javafx.util.Duration;

public abstract class AbstractPlayer extends BorderPane {

    public AbstractPlayer() {
        setStyle("-fx-background-color:#bfc2c7");
    }

    public final void play() {
        this.getMediaBar().updatePlayBtnIcon(AwesomeIcon.PAUSE);
        this.onPlay();
    }

    abstract public void play(int actionIdx);

    abstract protected void onPlay();

    public final void pause() {
        this.getMediaBar().updatePlayBtnIcon(AwesomeIcon.PLAY);
        this.onPause();
    }

    abstract protected void onPause();

    abstract public MediaPlayer.Status getStatus();

    abstract public Duration getCurrentTime();

    abstract public Duration getTotalDuration();

    abstract public void seekToStartTime();

    abstract public void seek(double seek);

    abstract public void setRate(double rate);

    abstract public void addCurrentTimeListener(InvalidationListener listener);

    abstract public void onEndOfSource(Runnable runnable);

    abstract public void setOnReady(Runnable runnable);

    abstract protected MediaBar getMediaBar();

    abstract public void updateStatus(MediaPlayer.Status newStatus);

    abstract public void onFinished();
}

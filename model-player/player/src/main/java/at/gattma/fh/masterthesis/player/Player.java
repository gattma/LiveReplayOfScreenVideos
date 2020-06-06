package at.gattma.fh.masterthesis.player;

import javafx.beans.property.ReadOnlyObjectProperty;
import javafx.scene.Node;
import javafx.scene.media.MediaPlayer;
import javafx.util.Duration;

public interface Player {

    void play();
    void pause();
    MediaPlayer.Status getStatus();
    Duration getCurrentTime();
    Duration getTotalDuration();
    void seekToStartTime();
    void seek(double seek);
    void setRate(double rate);
    ReadOnlyObjectProperty<Duration> currentTimeProperty();
    void onEndOfSource(Runnable runnable);
    void setOnReady(Runnable runnable);
    void setTop(Node node);
}

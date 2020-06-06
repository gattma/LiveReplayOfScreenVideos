package at.gattma.fh.masterthesis;

import at.gattma.fh.masterthesis.exceptions.ParseModelException;
import at.gattma.fh.masterthesis.util.Constants;
import at.gattma.fh.masterthesis.player.AbstractPlayer;
import at.gattma.fh.masterthesis.player.VideoPlayer;
import at.gattma.fh.masterthesis.player.VideoWorkflowPlayer;
import at.gattma.fh.masterthesis.player.WorkflowPlayer;
import at.gattma.fh.masterthesis.util.MessageUtil;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Scene;
import javafx.scene.control.Menu;
import javafx.scene.control.MenuBar;
import javafx.scene.control.MenuItem;
import javafx.scene.media.MediaPlayer;
import javafx.scene.paint.Color;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

import java.io.File;
import java.net.MalformedURLException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main extends Application implements NativeKeyListener {

    private AbstractPlayer videoPlayer;

    public void start(final Stage primaryStage) {
        MenuItem openVideo = new MenuItem("Play video");
        MenuItem openReplay = new MenuItem("Play .replay");
        MenuItem openVideoReplay = new MenuItem("Play video and .replay");
        Menu file = new Menu("File");
        file.getItems().add(openVideo);
        file.getItems().add(openReplay);
        file.getItems().add(openVideoReplay);

        MenuBar menu = new MenuBar();
        menu.getMenus().add(file);

        FileChooser fileChooser = new FileChooser();
        openVideo.setOnAction(e -> {
            if (videoPlayer != null) videoPlayer.pause();
            fileChooser.setTitle(Constants.OPEN_VIDEO_TITLE);
            fileChooser.getExtensionFilters().clear();
            fileChooser.getExtensionFilters().add(Constants.VIDEO_FILE_EXT);

            File video = fileChooser.showOpenDialog(primaryStage);
            if (video != null) {
                try {
                    videoPlayer = new VideoPlayer(video);
                    videoPlayer.setOnReady(primaryStage::sizeToScene);
                    videoPlayer.setTop(menu);
                    primaryStage.setScene(new Scene(videoPlayer, Color.BLACK));
                } catch (MalformedURLException | ParseModelException e1) {
                    System.err.printf("not able to parse replay file: %s%n", e1.getMessage());
                    MessageUtil.showErrorMessage(
                            "Error",
                            "Error parsing replay file",
                            String.format("Not able to parse replay file: %s", e1.getMessage())
                    );
                }
            }
        });

        openReplay.setOnAction(e -> {
            if (videoPlayer != null) videoPlayer.pause();
            fileChooser.setTitle(Constants.OPEN_REPLAY_TITLE);
            fileChooser.getExtensionFilters().clear();
            fileChooser.getExtensionFilters().add(Constants.REPLAY_FILE_EXT);

            File replay = fileChooser.showOpenDialog(primaryStage);
            if (replay != null) {
                try {
                    videoPlayer = new WorkflowPlayer(replay);
                    videoPlayer.setOnReady(primaryStage::sizeToScene);
                    videoPlayer.setTop(menu);
                    Scene s = new Scene(videoPlayer, Color.BLACK);
                    s.getStylesheets().add("style.css");
                    primaryStage.setScene(s);
                } catch (ParseModelException ex) {
                    System.err.printf("not able to parse replay file: %s%n", ex.getMessage());
                    MessageUtil.showErrorMessage(
                            "Error",
                            "Error parsing replay file",
                            String.format("Not able to parse replay file: %s", ex.getMessage())
                    );
                }

            }
        });


        openVideoReplay.setOnAction(e -> {
            if (videoPlayer != null) videoPlayer.pause();
            fileChooser.setTitle(Constants.OPEN_VIDEO_TITLE);
            fileChooser.getExtensionFilters().add(Constants.VIDEO_FILE_EXT);

            File video = fileChooser.showOpenDialog(primaryStage);
            if (video != null) {
                try {
                    videoPlayer = new VideoWorkflowPlayer(video);
                    videoPlayer.setOnReady(primaryStage::sizeToScene);
                    videoPlayer.setTop(menu);
                    primaryStage.setScene(new Scene(videoPlayer, Color.BLACK));
                } catch (MalformedURLException | ParseModelException e1) {
                    System.err.printf("not able to parse replay file: %s%n", e1.getMessage());
                    MessageUtil.showErrorMessage(
                            "Error",
                            "Error parsing replay file",
                            String.format("Not able to parse replay file: %s", e1.getMessage())
                    );
                }
            }
        });

        Scene scene = new Scene(menu, 200, 100, Color.BLACK);

        primaryStage.setScene(scene);
        primaryStage.show();
        primaryStage.setOnCloseRequest((we) -> {
            try {
                GlobalScreen.unregisterNativeHook();
            } catch (NativeHookException ex) {
                // IGNORE
            }
        });

        try {
            Logger logger = Logger.getLogger(GlobalScreen.class.getPackage().getName());
            logger.setLevel(Level.OFF);
            GlobalScreen.registerNativeHook();
            GlobalScreen.addNativeKeyListener(this);
        } catch (NativeHookException e) {
            // IGNORE
        }

    }

    private boolean ctrlPressed = false;
    public void nativeKeyPressed(NativeKeyEvent ev) {
        if (ev.getKeyCode() == NativeKeyEvent.VC_CONTROL) {
            ctrlPressed = true; // ctrl key is pressed
        }
    }

    @Override
    public void nativeKeyReleased(NativeKeyEvent ev) {
        if (ev.getKeyCode() == NativeKeyEvent.VC_CONTROL) ctrlPressed = false; // ctrl key is released
        if (ev.getKeyCode() == NativeKeyEvent.VC_P && ctrlPressed) {
            if (videoPlayer == null) return;

            Platform.runLater(() -> {
                if (videoPlayer.getStatus() == MediaPlayer.Status.PLAYING) {
                    videoPlayer.pause();
                } else {
                    videoPlayer.play();
                }
            });
        }
    }


    @Override
    public void nativeKeyTyped(NativeKeyEvent nativeKeyEvent) {
        // IGNORE
    }

    public static void main(String[] args) {
        launch(args);
    }
}

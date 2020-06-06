package at.gattma.fh.masterthesis.util;

import javafx.application.Platform;
import javafx.scene.control.Alert;

public class MessageUtil {

    public static void showErrorMessage(String title, String header, String content) {
        showMessage(title, header, content, Alert.AlertType.ERROR);
    }

    public static void showMessage(String title, String header, String content, Alert.AlertType type) {
        Platform.runLater(() -> {
            Alert alert = new Alert(type);
            alert.setTitle(title);
            alert.setHeaderText(header);
            alert.setContentText(content);
        });
    }
}

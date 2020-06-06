package at.gattma.fh.masterthesis.components;

import at.gattma.fh.masterthesis.util.Constants;
import at.gattma.fh.masterthesis.player.AbstractPlayer;
import de.jensd.fx.fontawesome.AwesomeDude;
import de.jensd.fx.fontawesome.AwesomeIcon;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Tooltip;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.Pane;

import java.io.File;

public class Card extends AnchorPane {

    public Card(String imgPath, String type, AbstractPlayer player, int actionIdx) {
        Pane pane = new Pane();
        pane.setPrefHeight(100);
        pane.setPrefWidth(23);
        pane.setStyle("-fx-background-color: #007390;");
        getChildren().add(pane);
        getChildren().addAll(
                newImage(imgPath),
                newLabel(182, 5, 40, 200, "custom-white-title-label", extractFilename(imgPath)),
                newLabel(182, 30, 31, 100, "custom-white-label", "Type: " + type),
                newButton(player, actionIdx)
        );

        setPrefHeight(30);
        setPrefWidth(180);
        setHeight(30);
        setWidth(150);
        setStyle("-fx-background-color: #00ADD8;");
        getStyleClass().add("card-unpadded");
        // <Label layoutX="182.0" layoutY="107.0" prefHeight="33.0" prefWidth="210.0" styleClass="custom-white-label" text="We need you." />
    }

    private String extractFilename(String path) {
        return path.substring(
                path.lastIndexOf(File.separator) + 1,
                path.indexOf(".png") + 4
        );
    }

    private ImageView newImage(String path) {
        ImageView img = new ImageView();
        img.setImage(new Image(String.format("file:///%s", path)));
        img.setLayoutX(50);
        img.setLayoutY(14);
        img.setFitWidth(80);
        img.setFitHeight(80);
        return img;
    }

    private Label newLabel(double x, double y, double height, double width, String style, String text) {
        Label l = new Label(text);
        l.setLayoutX(x);
        l.setLayoutY(y);
        l.setPrefHeight(height);
        l.setPrefWidth(width);
        l.getStyleClass().add(style);
        return l;
    }

    private Button newButton(AbstractPlayer player, int actionIdx) {
        Button b = new Button();
        b.setLayoutX(182);
        b.setLayoutY(65);
        Tooltip tooltip = new Tooltip("Forward");
        Tooltip.install(b, tooltip);
        AwesomeDude.setIcon(b, AwesomeIcon.FORWARD, Constants.ICON_SIZE);

        b.setOnAction(e -> player.play(actionIdx));
        return b;
    }
}

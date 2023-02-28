package dbp;

import javafx.fxml.*;
import javafx.application.Application;
import javafx.scene.*;
import javafx.stage.*;
import java.sql.Connection;

public class main extends Application {
				@Override
				public void start(Stage primaryStage) throws Exception {
								Parent root = FXMLLoader.load(getClass().getResource("main.fxml"));
								Scene scene = new Scene(root);
								primaryStage.setScene(scene);
								primaryStage.show();
				}
				public static void main(String[] args) {
								launch(args);
				}
}

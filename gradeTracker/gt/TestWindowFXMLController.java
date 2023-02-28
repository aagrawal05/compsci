package gt;

import java.time.LocalDate;
import javafx.event.ActionEvent;
import javafx.fxml.*;
import javafx.collections.*;
import javafx.scene.text.Text;
import javafx.scene.control.*;
import javafx.scene.*;
import javafx.stage.*;
import java.io.IOException;
import java.net.URL; 
import java.util.ResourceBundle;
import javafx.scene.control.Alert.AlertType;
import javafx.beans.value.*;

public class TestWindowFXMLController implements Initializable {
	
	@FXML
	private TextField nameField; 

	@FXML
	private ComboBox<String> subjectComboBox;
	
	@FXML
	private TextField scoreField;

	@FXML
	private TextField marksField;

	@FXML
	private DatePicker datePicker;

	@FXML
	private TextArea reflectionTextArea;

	@FXML
	protected void handleSubmitButtonAction(ActionEvent event) {
		System.out.println("New Test Added - ");
		System.err.println("Name: " + nameField.getText());
		System.err.println("Score: " + scoreField.getText());
		System.err.println("Marks: " + marksField.getText());
		System.err.println("Date: " + datePicker.getValue());
		System.err.println("Reflection: " + reflectionTextArea.getText());

		if (	
			datePicker.getValue() != null && 
			subjectComboBox.getValue() != null &&
			!nameField.getText().equals("") && 
			!reflectionTextArea.getText().equals("") &&
		   	isNumeric(marksField.getText()) &&
			isNumeric(scoreField.getText()) &&
			Integer.parseInt(marksField.getText()) >= Integer.parseInt(scoreField.getText())
		) {
			main.addTest(
				new Test(
					nameField.getText(), 
					reflectionTextArea.getText(), 
					subjectComboBox.getValue(), 
					datePicker.getValue(),
					Integer.parseInt(scoreField.getText()),
					Integer.parseInt(marksField.getText())
				)
			);
	
			((Stage)((Node) event.getSource()).getScene().getWindow()).close();
		} else {
			Alert a = new Alert(AlertType.WARNING, "Please fill in all fields correctly.");
			a.showAndWait();
		}
	}

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		assert nameField != null : "fx:id=\"nameField\" was not injected: check your FXML file 'TestWindow.fxml'.";
		assert subjectComboBox != null : "fx:id=\"subjectSelector\" was not injected: check your FXML file 'main.fxml'.";
		assert scoreField != null : "fx:id=\"scoreField\" was not injected: check your FXML file 'TestWindow.fxml'.";
		assert marksField != null : "fx:id=\"marksField\" was not injected: check your FXML file 'TestWindow.fxml'.";
		assert datePicker != null : "fx:id=\"datePicker\" was not injected: check your FXML file 'TestWindow.fxml'.";
		assert reflectionTextArea != null : "fx:id=\"reflectionTextArea\" was not injected: check your FXML file 'TestWindow.fxml'.";
		subjectComboBox.setItems(FXCollections.observableArrayList(main.getSubjects()));

		// Force the scoreField and marksFields to be numeric only by creating a change listener when the text changes
		scoreField.textProperty().addListener(new ChangeListener<String>() {
		    @Override
		    public void changed(ObservableValue<? extends String> observable, String oldValue, 
			String newValue) {
			if (!newValue.matches("\\d*")) {
			   scoreField.setText(newValue.replaceAll("[^\\d]", ""));
			}
		    }
		});

		marksField.textProperty().addListener(new ChangeListener<String>() {
		    @Override
		    public void changed(ObservableValue<? extends String> observable, String oldValue, 
			String newValue) {
			if (!newValue.matches("\\d*")) {
			   marksField.setText(newValue.replaceAll("[^\\d]", ""));
			}
		    }
		});
	}

	private boolean isNumeric(String strNum) {
	    	if (strNum == null) { return false; }
		try { int d = Integer.parseInt(strNum);} 
		catch (NumberFormatException nfe) { return false; }
		return true;
	}

}
